"""
You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.
The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.
This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.
Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.
In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

Start by tilting the lever so all of the rocks will slide north as far as they will go:
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.
The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.
Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

Your puzzle answer was 106997.

--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!
Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.
In the above example, after 1000000000 cycles, the total load on the north support beams is 64.
Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

Your puzzle answer was 99641.
"""
def calculate_total_load(grid):
    # Replacing the newline characters and converting the grid into a list of lists for easier manipulation
    grid = [list(row.strip()) for row in grid]
    num_rows = len(grid)
    num_cols = len(grid[0])

    # Function to move all rounded rocks north as far as they will go
    def move_rocks_north(grid):
        num_rows = len(grid)
        num_cols = len(grid[0])

        for col in range(num_cols):
            for row in range(1, num_rows):
                if grid[row][col] == 'O' and grid[row - 1][col] == '.':
                    # Find the furthest empty space above this rock
                    empty_space = row - 1
                    while empty_space > 0 and grid[empty_space - 1][col] == '.':
                        empty_space -= 1
                    # Move the rock to the empty space
                    grid[empty_space][col] = 'O'
                    grid[row][col] = '.'

    move_rocks_north(grid)

    # Calculate the total load on the north support beams
    total_load = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == 'O':
                # The load is equal to the number of rows from the rock to the south edge, including the rock's row
                total_load += (num_rows - row)

    return total_load


def spin_cycle(grid, cycles):
    def move_rocks_north():
        for col in range(num_cols):
            for row in range(1, num_rows):
                if grid[row][col] == 'O' and grid[row - 1][col] == '.':
                    empty_space = row - 1
                    while empty_space > 0 and grid[empty_space - 1][col] == '.':
                        empty_space -= 1
                    grid[empty_space][col] = 'O'
                    grid[row][col] = '.'

    def move_rocks_west():
        for row in range(num_rows):
            for col in range(1, num_cols):
                if grid[row][col] == 'O' and grid[row][col - 1] == '.':
                    empty_space = col - 1
                    while empty_space > 0 and grid[row][empty_space - 1] == '.':
                        empty_space -= 1
                    grid[row][empty_space] = 'O'
                    grid[row][col] = '.'

    def move_rocks_south():
        for col in range(num_cols):
            for row in range(num_rows - 2, -1, -1):
                if grid[row][col] == 'O' and grid[row + 1][col] == '.':
                    empty_space = row + 1
                    while empty_space < num_rows - 1 and grid[empty_space + 1][col] == '.':
                        empty_space += 1
                    grid[empty_space][col] = 'O'
                    grid[row][col] = '.'

    def move_rocks_east():
        for row in range(num_rows):
            for col in range(num_cols - 2, -1, -1):
                if grid[row][col] == 'O' and grid[row][col + 1] == '.':
                    empty_space = col + 1
                    while empty_space < num_cols - 1 and grid[row][empty_space + 1] == '.':
                        empty_space += 1
                    grid[row][empty_space] = 'O'
                    grid[row][col] = '.'

    # If the grid is already converted to a list of lists, this is unnecessary
    num_rows = len(grid)
    num_cols = len(grid[0])
    previous_states = []
    cycle_count = 0

    while cycle_count < cycles:
        # Perform a cycle
        move_rocks_north()
        move_rocks_west()
        move_rocks_south()
        move_rocks_east()


        # Calculate the total load on the north support beams
        total_load = sum(row.count('O') * (num_rows - idx) for idx, row in enumerate(grid))

        # Create a string representation of the grid to check for repeats
        grid_str = ''.join(''.join(row) for row in grid)
        if grid_str in previous_states:
            # A repeat has been found, break out and calculate based on periodicity
            cycle_length = cycle_count - list(previous_states).index(grid_str)
            remaining_cycles = (cycles - cycle_count) % cycle_length - 1
            return spin_cycle(grid, remaining_cycles)
        else:
            previous_states.append(grid_str)
            previous_states = list(dict.fromkeys(previous_states))

        cycle_count += 1

    # Calculate the total load on the north support beams
    total_load = sum(row.count('O') * (num_rows - idx) for idx, row in enumerate(grid))

    return total_load


with open('input.txt', 'r') as file:
    puzzle_input = file.readlines()
    grid = [list(row.strip()) for row in puzzle_input]

    # Calculating the total load for the given puzzle input
    total_load = calculate_total_load(puzzle_input)

    # Calculating the total load after 1000000000 cycles
    total_load_cycles = spin_cycle(grid, 1000000000)

    print("First puzzle solution:", total_load)
    print("Second puzzle solution:", total_load_cycles)

