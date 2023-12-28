"""
--- Day 22: Sand Slabs ---
Enough sand has fallen; it can finally filter water for Snow Island.

Well, almost.

The sand has been falling as large compacted bricks of sand, piling up to form an impressive stack here near the edge of Island Island. In order to make use of the sand to filter water, some of the bricks will need to be broken apart - nay, disintegrated - back into freely flowing sand.

The stack is tall enough that you'll have to be careful about choosing which bricks to disintegrate; if you disintegrate the wrong brick, large portions of the stack could topple, which sounds pretty dangerous.

The Elves responsible for water filtering operations took a snapshot of the bricks while they were still falling (your puzzle input) which should let you work out which bricks are safe to disintegrate. For example:

1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
Each line of text in the snapshot represents the position of a single brick at the time the snapshot was taken. The position is given as two x,y,z coordinates - one for each end of the brick - separated by a tilde (~). Each brick is made up of a single straight line of cubes, and the Elves were even careful to choose a time for the snapshot that had all of the free-falling bricks at integer positions above the ground, so the whole snapshot is aligned to a three-dimensional cube grid.

A line like 2,2,2~2,2,2 means that both ends of the brick are at the same coordinate - in other words, that the brick is a single cube.

Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks that are two cubes in volume, both oriented horizontally. The first brick extends in the x direction, while the second brick extends in the y direction.

A line like 0,0,1~0,0,10 represents a ten-cube brick which is oriented vertically. One end of the brick is the cube located at 0,0,1, while the other end of the brick is located directly above it at 0,0,10.

The ground is at z=0 and is perfectly flat; the lowest z value a brick can have is therefore 1. So, 5,5,1~5,6,1 and 0,2,1~0,2,5 are both resting on the ground, but 3,3,2~3,3,3 was above the ground at the time of the snapshot.

Because the snapshot was taken while the bricks were still falling, some bricks will still be in the air; you'll need to start by figuring out where they will end up. Bricks are magically stabilized, so they never rotate, even in weird situations like where a long horizontal brick is only supported on one end. Two bricks cannot occupy the same position, so a falling brick will come to rest upon the first other brick it encounters.

Here is the same example again, this time with each brick given a letter so it can be marked in diagrams:

1,0,1~1,2,1   <- A
0,0,2~2,0,2   <- B
0,2,3~2,2,3   <- C
0,0,4~0,2,4   <- D
2,0,5~2,2,5   <- E
0,1,6~2,1,6   <- F
1,1,8~1,1,9   <- G
At the time of the snapshot, from the side so the x axis goes left to right, these bricks are arranged like this:

 x
012
.G. 9
.G. 8
... 7
FFF 6
..E 5 z
D.. 4
CCC 3
BBB 2
.A. 1
--- 0
Rotating the perspective 90 degrees so the y axis now goes left to right, the same bricks are arranged like this:

 y
012
.G. 9
.G. 8
... 7
.F. 6
EEE 5 z
DDD 4
..C 3
B.. 2
AAA 1
--- 0
Once all of the bricks fall downward as far as they can go, the stack looks like this, where ? means bricks are hidden behind other bricks at that location:

 x
012
.G. 6
.G. 5
FFF 4
D.E 3 z
??? 2
.A. 1
--- 0
Again from the side:

 y
012
.G. 6
.G. 5
.F. 4
??? 3 z
B.C 2
AAA 1
--- 0
Now that all of the bricks have settled, it becomes easier to tell which bricks are supporting which other bricks:

Brick A is the only brick supporting bricks B and C.
Brick B is one of two bricks supporting brick D and brick E.
Brick C is the other brick supporting brick D and brick E.
Brick D supports brick F.
Brick E also supports brick F.
Brick F supports brick G.
Brick G isn't supporting any bricks.
Your first task is to figure out which bricks are safe to disintegrate. A brick can be safely disintegrated if, after removing it, no other bricks would fall further directly downward. Don't actually disintegrate any bricks - just determine what would happen if, for each brick, only that brick were disintegrated. Bricks can be disintegrated even if they're completely surrounded by other bricks; you can squeeze between bricks if you need to.

In this example, the bricks can be disintegrated as follows:

Brick A cannot be disintegrated safely; if it were disintegrated, bricks B and C would both fall.
Brick B can be disintegrated; the bricks above it (D and E) would still be supported by brick C.
Brick C can be disintegrated; the bricks above it (D and E) would still be supported by brick B.
Brick D can be disintegrated; the brick above it (F) would still be supported by brick E.
Brick E can be disintegrated; the brick above it (F) would still be supported by brick D.
Brick F cannot be disintegrated; the brick above it (G) would fall.
Brick G can be disintegrated; it does not support any other bricks.
So, in this example, 5 bricks can be safely disintegrated.

Figure how the blocks will settle based on the snapshot. Once they've settled, consider disintegrating a single brick; how many bricks could be safely chosen as the one to get disintegrated?

Your puzzle answer was 468.

--- Part Two ---
Disintegrating bricks one at a time isn't going to be fast enough. While it might sound dangerous, what you really need is a chain reaction.

You'll need to figure out the best brick to disintegrate. For each brick, determine how many other bricks would fall if that brick were disintegrated.

Using the same example as above:

Disintegrating brick A would cause all 6 other bricks to fall.
Disintegrating brick F would cause only 1 other brick, G, to fall.
Disintegrating any other brick would cause no other bricks to fall. So, in this example, the sum of the number of other bricks that would fall as a result of disintegrating each brick is 7.

For each brick, determine how many other bricks would fall if that brick were disintegrated. What is the sum of the number of other bricks that would fall?

Your puzzle answer was 75358.
"""
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

