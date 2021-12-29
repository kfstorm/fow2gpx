import sys
import logging
import argparse

from parser import FogMap, _tile_x_y_to_lng_lat, BLOCK_BITMAP_SIZE
import gpxpy
import gpxpy.gpx

BLOCK_WIDTH = 64
assert BLOCK_WIDTH**2 == BLOCK_BITMAP_SIZE * 8


def get_points(map):
    for _, tile in map.tile_map.items():
        for _, block in tile.blocks.items():
            for x in range(BLOCK_WIDTH):
                for y in range(BLOCK_WIDTH):
                    offset = y * BLOCK_WIDTH + x
                    if block.bitmap[offset // 8] & (1 << (7 - offset % 8)):
                        yield _tile_x_y_to_lng_lat(
                            tile.x + block.x / 128 + x / 128 / 64,
                            tile.y + block.y / 128 + y / 128 / 64)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(
        description='Export your Fog of World track data to GPX files.')
    parser.add_argument(
        '--fow-path',
        "-i",
        type=str,
        help="The path of Fog of World data folder. "
        "Note that this folder must contains the 'Sync' folder.",
        required=True,
    )
    parser.add_argument(
        '--output-file',
        '-o',
        type=argparse.FileType('w', encoding='UTF-8'),
        help="The path of exported GPX file.",
        required=True,
    )
    parser.epilog = 'Example: python main.py -i "/path/to/Fog of World" -o "/path/to/output.gpx"'

    args = parser.parse_args()

    logging.info("Loading Fog of World data...")
    map = FogMap(args.fow_path)
    logging.info("Fog of World data loaded.")

    logging.info("Gathering waypoints...")
    gpx = gpxpy.gpx.GPX()
    for lng, lat in get_points(map):
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(lat, lng))

    logging.info("Waypoints gathered. Writting output file...")
    args.output_file.write(gpx.to_xml())
