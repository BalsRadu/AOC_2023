"""
--- Day 18: Lavaduct Lagoon ---
Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?

Your puzzle answer was 70026.

--- Part Two ---
The Elves were right to be concerned; the planned lagoon would be much too small.

After a few minutes, someone realizes what happened; someone swapped the color and instruction parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.

Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

So, in the above example, the hexadecimal codes can be converted into the true instructions:

#70c710 = R 461937
#0dc571 = D 56407
#5713f0 = R 356671
#d2c081 = D 863240
#59c680 = R 367720
#411b91 = D 266681
#8ceee2 = L 577262
#caa173 = U 829975
#1b58a2 = L 112010
#caa171 = D 829975
#7807d2 = L 491645
#a77fa3 = U 686074
#015232 = L 5411
#7a21e3 = U 500254
Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115 cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan, how many cubic meters of lava could the lagoon hold?

Your puzzle answer was 68548301037382.
"""
from collections import deque, OrderedDict

def parse_instructions(input_data):

    """ Parse the input data into a list of instructions. """
    instructions = []
    hex_instructions = []
    for line in input_data.strip().split('\n'):
        direction, distance, hex_code = line.split()
        hex_code = hex_code[2:-1]  # Remove the parentheses
         # Extract the distance and direction from the hex code
        hex_distance = int(hex_code[:5], 16)
        direction_code = int(hex_code[5], 16)
        hex_direction = "RDLU"[direction_code]  # Map 0, 1, 2, 3 to 'R', 'D', 'L', 'U'

        hex_instructions.append((hex_direction, hex_distance))
        instructions.append((direction, int(distance)))

    return instructions, hex_instructions

def create_trench_map(instructions):
    """ Create a map of the trench based on the instructions and shift all points to positive coordinates. """
    x, y = 0, 0  # Starting position
    trench_map = OrderedDict()

    # Process each instruction
    for direction, distance in instructions:
        for _ in range(distance):
            if direction == 'R':
                x += 1
            elif direction == 'U':
                y -= 1
            elif direction == 'L':
                x -= 1
            elif direction == 'D':
                y += 1

            if y in trench_map:
                trench_map[y].append(x)
            else:
                trench_map[y] = [x]

    # Calculate the shift needed to make all coordinates positive
    min_x = min(min(x) for x in trench_map.values())
    min_y = min(trench_map.keys())

    # Apply the shift to all points in the trench map
    shifted_trench_map = OrderedDict()
    for y, row in trench_map.items():
        shifted_trench_map[y - min_y] = [x - min_x for x in row]

    # Sort the trench map by y-coordinate and then x-coordinate
    sorted_trench_map = OrderedDict()
    for y in sorted(shifted_trench_map.keys()):
        sorted_trench_map[y] = sorted(shifted_trench_map[y])

    return sorted_trench_map

def is_part_of_trench(x, y, trench_map):
    """ Check if the given point is part of the trench. """
    if y in trench_map:
        return x in trench_map[y]
    return False

def flood_fill(trench_map, start):
    """
    Fill the interior of the trench using an iterative, queue-based flood fill algorithm.
    Maybe this is a bit overkill for this problem, but i wanted to implement a flood fill algorithm
    since the day 10 puzzle.
    """
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Possible directions (R, D, L, U)
    to_fill = deque([start])
    filled = set()

    while to_fill:
        x, y = to_fill.popleft()
        if (x, y) not in filled and not is_part_of_trench(x, y, trench_map):
            filled.add((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                to_fill.append((nx, ny))

    return filled


def find_starting_point(trench_map):
    """ Find a point inside the trench loop. """
    # Start at the top of the map with the minimum y-coordinate
    for y in trench_map.keys():
        for i in range(len(trench_map[y]) - 1):
            if trench_map[y][i + 1] - trench_map[y][i] > 1:
                return (trench_map[y][i] + 1, y)

def calculate_lava_volume(instructions):
    """ Calculate the volume of lava the lagoon can hold. """

    trench_map = create_trench_map(instructions)

    # Find the starting point for flood fill
    start = find_starting_point(trench_map)

    # # Apply flood fill to find the interior area
    filled_area = flood_fill(trench_map, start)

    # Return the total area of the filled area and the trench
    return len(filled_area) + sum(len(row) for row in trench_map.values())

#------------------------------------------------------------------------------------------------------------------------------------
import math

def calculate_coordinates(instructions):
    """ Calculate the coordinates for each instruction point. """
    x, y = 0, 0  # Starting position
    coordinates = [(x, y)]  # Starting point

    # Process each instruction
    for direction, distance in instructions:
        if direction == 'R':
            x += distance
        elif direction == 'U':
            y -= distance
        elif direction == 'L':
            x -= distance
        elif direction == 'D':
            y += distance

        coordinates.append((x, y))

    return coordinates

def calculate_points_on_border(coordinates):
    """ Calculate the number of points on the border of the polygon. """
    border_points = 0
    for i in range(len(coordinates) - 1):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        # Greatest common divisor of dx and dy will give the number of points
        gcd = math.gcd(dx, dy)
        border_points += gcd

    return border_points

def calculate_polygon_area(coordinates):
    """ Calculate the area of a polygon using the shoelace formula. """
    n = len(coordinates)
    area = 0
    for i in range(n):
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[(i + 1) % n]  # Ensuring circular indexing
        area += (x1 * y2 - x2 * y1)

    return abs(area) / 2

def calculate_lava_volume_hex(hex_instructions):
    """
    Calculate the volume of lava the lagoon can hold based on hex instructions.
    The algorithm first converts hex instructions into coordinates of each point along the border of a polygonal shape. These coordinates are obtained by iterating through each instruction and updating the x and y positions accordingly.
    Once the coordinates are determined, the number of lattice points on the border of the polygon is calculated. This is achieved by examining each pair of consecutive points (forming a line segment) and using the slope of these segments.
    For segments with an integer slope, the number of lattice points is directly calculated. For non-integer slopes, the method involves finding a scaling factor that converts the slope into an integer, then determining the number of lattice points based on this scaled slope.
    After finding the number of border points, the area of the polygon is calculated using the shoelace formula. This formula computes the area based on the x and y coordinates of the vertices of the polygon.
    Finally, Pick's Theorem is applied to determine the number of interior points of the polygon. Pick's Theorem states that the area of a polygon equals the number of interior lattice points plus half the number of lattice points on the border, minus one.
    By rearranging this theorem, the number of interior points is found, which, when added to the number of border points, gives the total volume of lava the lagoon can hold.
    The solution was inspired by this post: https://math.stackexchange.com/questions/848976/how-to-calculate-the-number-of-lattice-points-in-the-interior-and-on-the-boundar
    """
    # Calculate the coordinates for each instruction point
    coordinates = calculate_coordinates(hex_instructions)

    # Calculate the number of points on the border
    border_points = calculate_points_on_border(coordinates)

    # Calculate the area of the polygon
    polygon_area = calculate_polygon_area(coordinates)

    # Calculate the number of interior points using Pick's Theorem: A = i + b/2 - 1
    interior_points = polygon_area - border_points / 2 + 1

    # The total volume of lava the lagoon can hold
    return int(interior_points + border_points)

with open('input.txt', 'r') as f:
    input_data = f.read()
    # Parse the input data into a list of instructions
    instructions, hex_instructions = parse_instructions(input_data)

    # # Calculate the volume of lava
    lava_volume = calculate_lava_volume(instructions)

    # Calculate the volume of lava using hex codes
    lava_volume_hex = calculate_lava_volume_hex(hex_instructions)

    print("First puzzle solution:", lava_volume)
    print("Second puzzle solution:", lava_volume_hex)

