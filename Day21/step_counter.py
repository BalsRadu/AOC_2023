"""
You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid trip to Desert Island! It even helpfully drops you off near the gardener and his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.), and rocks (#). For example:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take one step north, south, east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked O:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
Then, he takes a second step. Since at this point he could be at either tile marked O, his second step would allow him to reach any garden plot that is one step north, south, east, or west of any tile that he could have reached after the first step:

...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
After two steps, he could be at any of the tiles marked O above, including the starting position (either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
He will continue like this until his steps for the day have been exhausted. After a total of 6 steps, he could reach any of the garden plots marked O:

...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to reach any of 16 garden plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?

Your puzzle answer was 3660.

--- Part Two ---
The Elf seems confused by your answer until he realizes his mistake: he was reading from a list of his favorite numbers that are both perfect squares and perfect cubes, not his step counter.

The actual number of steps he needs to get today is exactly 26501365.

He also points out that the garden plots and rocks are set up so that the map repeats infinitely in every direction.

So, if you were to look one additional map-width or map-height out from the edge of the example map above, you would find that it keeps repeating:

.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden plots and rocks repeat as far as you can see. The Elf still starts on the one middle tile marked S, though - every other repeated S is replaced with a normal garden plot (.).

Here are the number of reachable garden plots in this new infinite version of the example map for different numbers of steps:

In exactly 6 steps, he can still reach 16 garden plots.
In exactly 10 steps, he can reach any of 50 garden plots.
In exactly 50 steps, he can reach 1594 garden plots.
In exactly 100 steps, he can reach 6536 garden plots.
In exactly 500 steps, he can reach 167004 garden plots.
In exactly 1000 steps, he can reach 668697 garden plots.
In exactly 5000 steps, he can reach 16733044 garden plots.
However, the step count the Elf needs is much larger! Starting from the garden plot marked S on your infinite map, how many garden plots could the Elf reach in exactly 26501365 steps?

Your puzzle answer was 605492675373144.
"""
from collections import deque

def find_start_pos(grid):
    """
    Iterates through the grid to locate the starting position marked by 'S'.
    """
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                return (i, j)
    return None

def parse_input(map_data):
    """
    Converts the input map data into a 2D grid and finds the starting position.
    """
    grid = [list(row.strip()) for row in map_data]
    start_pos = find_start_pos(grid)
    return grid, start_pos

def count_reachable_plots(grid, start_pos, steps):
    """
    Uses Breadth-First Search (BFS) to explore the garden grid. It counts the garden plots
    that can be reached exactly in the given number of steps, accounting for the infinite
    repeating nature of the grid. It tracks visited positions to avoid redundant calculations.
    """
    grid_height = len(grid)
    grid_width = len(grid[0])

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    visited = set()
    queue = deque([(start_pos, 0)])
    reachable_plots_count = 0

    while queue:
        pos, dist = queue.popleft()
        if dist == (steps + 1) or pos in visited:
            continue

        visited.add(pos)

        if (pos[0] + pos[1]) % 2 == steps % 2:
            reachable_plots_count += 1

        for d in directions:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if grid[new_pos[1] % grid_height][new_pos[0] % grid_width] != '#':
                queue.append((new_pos, dist + 1))

    return reachable_plots_count


def lagrange(x0, y0, x1, y1, x2, y2):
    """
    Implements Lagrange's polynomial interpolation to estimate the number of reachable plots
    for a significantly larger step count, based on known values for smaller step counts.
    """
    def polynomial(x):
        t0 = ((x - x1) * (x - x2)) // ((x0 - x1) * (x0 - x2)) * y0
        t1 = ((x - x0) * (x - x2)) // ((x1 - x0) * (x1 - x2)) * y1
        t2 = ((x - x0) * (x - x1)) // ((x2 - x0) * (x2 - x1)) * y2
        return t0 + t1 + t2
    return polynomial


with open('input.txt', 'r') as f:
    map_data = f.readlines()
    grid, start_pos = parse_input(map_data)

    # Count the number of reachable plots for 64 steps.
    number_of_plots = count_reachable_plots(map_data, start_pos, 64)

    # Find the number of reachable plots for 26501365 steps for an infinite grid.
    length_of_grid = len(grid[0])
    distance_to_edge = length_of_grid // 2

    x = [distance_to_edge + i * length_of_grid for i in range(3)]
    y = [count_reachable_plots(grid, start_pos, i) for i in x]


    polynomial = lagrange(x[0], y[0], x[1], y[1], x[2], y[2])

    print("First puzzle solution:", number_of_plots)
    print("Second puzzle solution:", polynomial(26501365))
