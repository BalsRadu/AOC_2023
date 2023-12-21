"""
The lava starts flowing rapidly once the Lava Production Facility is operational. As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: half of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall. Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles become very difficult to steer at high speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll need to find the best way to get the crucible from the lava pool to the machine parts factory. To do this, you need to minimize heat loss while choosing a route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, what is the least heat loss it can incur?

Your puzzle answer was 1013.

--- Part Two ---
The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory. Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end). However, it will eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
In the above example, an ultra crucible would incur the minimum possible heat loss of 94.

Here's another example:

111111111111
999999999991
999999999991
999999999991
999999999991
Sadly, an ultra crucible would need to take an unfortunate path like this one:

1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, what is the least heat loss it can incur?

Your puzzle answer was 1215.
"""
from collections import defaultdict
import heapq

def is_valid_position(y, x, grid):
    """ Check if the position is within the grid boundaries. """
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def get_neighbors(y, x, grid):
    """ Get neighboring positions of a cell in the grid. """
    for dy, dx in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        ny, nx = y + dy, x + dx
        if is_valid_position(ny, nx, grid):
            yield ny, nx

def calculate_heuristic(y, x, score, grid):
    """ Calculate the heuristic value for A* search. """
    return (len(grid) - y) + (len(grid[0]) - x) + score

def find_path(grid, min_step_number, max_step_number):
    """
    Find the minimum heat loss path in a grid using the A* search algorithm.

    This function implements the A* search algorithm to find a path from the
    top-left corner to the bottom-right corner of a grid. The path is chosen
    such that it minimizes the sum of the values (representing heat loss) of
    the cells it passes through. The path can only move horizontally or vertically.
    The path must be between 'min_step_number' and 'max_step_number' cells in length in each direction
    before it can change direction.
    """
    visited = defaultdict(lambda: float('inf'))
    queue = [(calculate_heuristic(0, 0, 0, grid), 0, (0, 0), 2)]
    target = (len(grid) - 1, len(grid[0]) - 1)

    while queue:
        _, score, (y, x), direction = heapq.heappop(queue)
        if (y, x) == target:
            return score

        for j, i in get_neighbors(y, x, grid):
            dy, dx = j - y, i - x
            if (dy == 0 and direction == 0) or (dx == 0 and direction == 1):
                continue

            new_score = 0
            for size in range(1, max_step_number + 1):
                ny, nx = y + size * dy, x + size * dx
                if not is_valid_position(ny, nx, grid):
                    break
                new_score += grid[ny][nx]
                total_score = score + new_score
                heuristic_value = calculate_heuristic(ny, nx, total_score, grid) + total_score
                position = ((ny, nx), 0 if dy == 0 else 1)

                if size >= min_step_number and heuristic_value < visited[position]:
                    heapq.heappush(queue, (heuristic_value, total_score, (ny, nx), 0 if dy == 0 else 1))
                    visited[position] = heuristic_value

with open('input.txt', 'r') as file:
    input_data = file.read()
    # Parsing the input data into a list of strings
    grid_lines = input_data.strip().split('\n')
    # Parsing the input data into a list of lists
    grid_list = [list(map(int, line)) for line in grid_lines]

    # Finding the minimum heat loss paths
    min_heat_los_no_numpy = find_path(grid_list, 1, 3)
    min_heat_loss_ultra_crucible = find_path(grid_list, 4, 10)

    print("First puzzle solution is: {0}".format(min_heat_los_no_numpy))
    print("Second puzzle solution is: {0}".format(min_heat_loss_ultra_crucible))

