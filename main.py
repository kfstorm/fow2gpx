import logging
import argparse
import math

from parser import FogMap, _tile_x_y_to_lng_lat, MAP_WIDTH, TILE_WIDTH, BITMAP_WIDTH, BLOCK_BITMAP_SIZE
import gpxpy
import gpxpy.gpx

try:
    import tqdm
except ModuleNotFoundError:
    tqdm = None

assert BITMAP_WIDTH**2 == BLOCK_BITMAP_SIZE * 8
SAMPLE_LEVEL_MAX = int(math.log(BITMAP_WIDTH, 2))
EARTH_EQUATOR_PERIMETER_METERS = 40_075_000


def get_points(map, slot_width):
    assert slot_width <= BITMAP_WIDTH
    assert BITMAP_WIDTH % slot_width == 0

    if tqdm:
        progress = tqdm.tqdm(
            total=sum([len(tile.blocks) for tile in map.tile_map.values()]))
    else:
        progress = None
    for _, tile in map.tile_map.items():
        for _, block in tile.blocks.items():
            slots = {}
            for y in range(BITMAP_WIDTH):
                for x in range(BITMAP_WIDTH):
                    slot_key = (x // slot_width, y // slot_width)
                    if slot_key in slots:
                        continue
                    offset = y * BITMAP_WIDTH + x
                    if block.bitmap[offset // 8] & (1 << (7 - offset % 8)):
                        slots[slot_key] = (x, y)
            for _, sample in slots.items():
                yield _tile_x_y_to_lng_lat(
                    tile.x + block.x / 128 + sample[0] / 128 / 64,
                    tile.y + block.y / 128 + sample[1] / 128 / 64)
            if progress:
                progress.update(1)


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

    def get_slot_width(sample_level):
        return int(math.pow(2, sample_level))

    def get_resolution(sample_level):
        return int(EARTH_EQUATOR_PERIMETER_METERS / MAP_WIDTH / TILE_WIDTH /
                   BITMAP_WIDTH * get_slot_width(sample_level))

    sample_level_text = "0 means no sampling. " + " ".join([
        f'{i} means resolution of ~{get_resolution(i)}m.'
        for i in range(1, SAMPLE_LEVEL_MAX + 1)
    ])

    parser.add_argument(
        '--sample-level',
        '-s',
        type=int,
        default=0,
        metavar=f"[0-{SAMPLE_LEVEL_MAX}]",
        choices=range(0, SAMPLE_LEVEL_MAX + 1),
        help=
        "The optional sample level to reduce the amount of waypoints and the size of output file. "
        f"Must be between 0 - {SAMPLE_LEVEL_MAX}. " + sample_level_text,
        required=False,
    )
    parser.epilog = 'Example: python main.py -i "/path/to/Fog of World" -o "/path/to/output.gpx"'

    args = parser.parse_args()

    logging.info("Loading Fog of World data...")
    map = FogMap(args.fow_path)
    logging.info("Fog of World data loaded.")

    logging.info("Gathering waypoints...")
    gpx = gpxpy.gpx.GPX()
    for lng, lat in get_points(map, get_slot_width(args.sample_level)):
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(lat, lng))

    logging.info("Waypoints gathered. Writting GPX file...")
    args.output_file.write(gpx.to_xml())
