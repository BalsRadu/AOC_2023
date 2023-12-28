import re
import itertools
from functools import reduce

def parse_input(input_lines):
    """Parse the input lines into a list of bricks, each brick is a tuple of three ranges (x, y, z)"""
    def parse_line(line):
        match = re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line)
        if match:
            xl, yl, zl, xr, yr, zr = map(int, match.groups())
            return range(xl, xr + 1), range(yl, yr + 1), range(zl, zr + 1)
        return None

    return list(filter(None, map(parse_line, input_lines)))

def drop(bricks):
    """
    Simulates dropping a set of bricks into a 3D space. This function calculates the final position of each brick
    after considering the positions of previously dropped bricks. It ensures that bricks stack on top of each other
    without overlapping in the z-axis.
    """
    def drop_single_brick(acc, brick):
        z_cache, dropped = acc
        xs, ys, zs = brick
        lowest_z = 1 + max([z_cache.get((x, y), 0) for x in xs for y in ys])
        new_zs = range(lowest_z, lowest_z + len(zs))
        new_brick = (xs, ys, new_zs)
        updated_z_cache = {**z_cache, **{(x, y): max(z_cache.get((x, y), 0), new_zs.stop - 1) for x in xs for y in ys}}
        return updated_z_cache, dropped + [new_brick]

    _, dropped_bricks = reduce(drop_single_brick, sorted(bricks, key=lambda b: min(b[2])), ({}, []))
    return dropped_bricks

def supports(brick, other):
    """
    Determines if one brick supports another brick. A brick supports another if they overlap in the x and y axes,
    and the top of the supporting brick is directly below the bottom of the supported brick.
    """
    lx, ly, lz = brick
    rx, ry, rz = other
    return lz.stop == rz.start and not set(lx).isdisjoint(rx) and not set(ly).isdisjoint(ry)

def build_support_maps(bricks):
    """
    Builds two maps from a list of bricks: one indicating which bricks are supported by a given brick (supports_map),
    and the other showing which bricks support a given brick (supported_by_map).
    """
    supports_map = {brick: set(filter(lambda other: supports(brick, other), bricks)) for brick in bricks}
    supported_by_map = {brick: set(filter(lambda other: supports(other, brick), bricks)) for brick in bricks}
    return supports_map, supported_by_map

def count_safe_bricks(dropped_bricks, supports_map, supported_by_map):
    """
    Counts the number of bricks that can be safely removed without causing any other bricks to fall.
    A brick can be safely removed if it either supports no other bricks or all bricks it supports are also
    supported by other bricks.
    """
    return len([brick for brick in dropped_bricks if not supports_map[brick] or all(len(supported_by_map[supported]) > 1 for supported in supports_map[brick])])

def find_unsupported_bricks(supported_by_map):
    """
    Identifies bricks that are unsupported or solely supported. These bricks are critical as their removal
    might cause other bricks to fall. The function returns a set of such bricks.
    """
    return set(itertools.chain.from_iterable(filter(lambda s: len(s) == 1, supported_by_map.values())))

def count_falling_bricks(brick, supports_map, supported_by_map):
    """
    Estimates the number of bricks that would fall if a given brick is removed. It simulates the removal of the brick
    and counts how many bricks lose their support as a consequence, considering the cascading effect of falling bricks.
    """
    def estimate_brick_fall(brick, supported_by_map):
        queue = [brick]
        count = 0
        while queue:
            current_brick = queue.pop(0)
            lost_support_bricks = supports_map.get(current_brick, set())
            for ls_brick in lost_support_bricks:
                supported_by_map[ls_brick].discard(current_brick)
                if not supported_by_map[ls_brick]:
                    queue.append(ls_brick)
                    count += 1
        return count

    # Create a copy of supported_by_map to avoid modifying the original during simulation
    supported_by_map_copy = {key: set(val) for key, val in supported_by_map.items()}
    return estimate_brick_fall(brick, supported_by_map_copy)

with open("input.txt", 'r') as file:
    input_lines = file.read().splitlines()

    # Count the number of bricks that are safe to remove
    bricks = parse_input(input_lines)
    dropped_bricks = drop(bricks)
    supports_map, supported_by_map = build_support_maps(dropped_bricks)
    bricks_number = count_safe_bricks(dropped_bricks, supports_map, supported_by_map)

    # Recalculating the total number of falling bricks for each brick with the revised approach
    total_falling_bricks_count = sum([count_falling_bricks(brick, supports_map, supported_by_map) for brick in find_unsupported_bricks(supported_by_map)])

    print("Fisrt puzzle solution:", bricks_number)
    print("Second puzzle solution:", total_falling_bricks_count)

