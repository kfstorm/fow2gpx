import sys

from parser import FogMap, _tile_x_y_to_lng_lat, BLOCK_BITMAP_SIZE
import gpxpy
import gpxpy.gpx

BLOCK_WIDTH = 64
assert BLOCK_WIDTH ** 2 == BLOCK_BITMAP_SIZE * 8

def get_points(map):
    for _, tile in map.tile_map.items():
        for _, block in tile.blocks.items():
            for x in range(BLOCK_WIDTH):
                for y in range(BLOCK_WIDTH):
                    offset = y * BLOCK_WIDTH + x
                    if block.bitmap[offset // 8] & (1 << (7 - offset % 8)):
                        yield _tile_x_y_to_lng_lat(tile.x + block.x / 128 + x / 128 / 64, tile.y + block.y / 128 + y / 128 / 64)

if __name__ == "__main__":
    assert len(sys.argv) > 2
    gpx = gpxpy.gpx.GPX()
    map = FogMap(sys.argv[1])
    for lng, lat in get_points(map):
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(lat, lng))

    with open(sys.argv[2], "w", encoding="utf8") as f:
        f.write(gpx.to_xml())
