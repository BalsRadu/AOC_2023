def parse_map(input_data):
    """ Parses the input data into a map format """
    return [list(line) for line in input_data.splitlines()]

def expand_universe(map):
    """ Expands the universe by adding empty rows and columns adjacent to each empty row or column """
    expanded_map = []

    # Add an empty row below each empty row
    for row in map:
        expanded_map.append(row)
        if all(cell == '.' for cell in row):
            expanded_map.append(['.'] * len(row))

    # Transpose to add columns
    transposed_map = list(zip(*expanded_map))
    expanded_transposed_map = []

    # Add an empty column to the right of each empty column
    for col in transposed_map:
        expanded_transposed_map.append(col)
        if all(cell == '.' for cell in col):
            expanded_transposed_map.append(tuple('.' for _ in col))

    # Transpose back to original format
    return [list(row) for row in zip(*expanded_transposed_map)]

def identify_galaxies(map):
    """ Identifies galaxies and stores their coordinates """
    galaxies = {}
    galaxy_number = 1
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell != '.':
                galaxies[galaxy_number] = (x, y)
                galaxy_number += 1
    return galaxies

def calculate_distances(galaxies):
    """ Calculate the Manhattan distances between all unique pairs of galaxies """
    from itertools import combinations

    total_distance = 0
    for (g1, coord1), (g2, coord2) in combinations(galaxies.items(), 2):
        distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
        total_distance += distance

    return total_distance


def get_scaled_coordinates(galaxies, map, scaling_factor):
    """ Calculate the scaled coordinates of each galaxy, accounting for the expanded size of empty rows and columns """
    scaled_galaxies = {}

    # Count the number of empty rows and columns before each point in the map
    empty_rows_count = [0] * len(map)
    for i in range(1, len(map)):
        empty_rows_count[i] = empty_rows_count[i - 1] + (1 if all(cell == '.' for cell in map[i - 1]) else 0)

    empty_cols_count = [0] * len(map[0])
    for j in range(1, len(map[0])):
        empty_cols_count[j] = empty_cols_count[j - 1] + (1 if all(map[i][j - 1] == '.' for i in range(len(map))) else 0)

    # Scale the coordinates of each galaxy
    for galaxy, (x, y) in galaxies.items():
        scaled_x = x + empty_cols_count[min(x, len(empty_cols_count) - 1)] * (scaling_factor - 1)
        scaled_y = y + empty_rows_count[min(y, len(empty_rows_count) - 1)] * (scaling_factor - 1)
        scaled_galaxies[galaxy] = (scaled_x, scaled_y)

    return scaled_galaxies



with open("input.txt") as file:
    # Parse the map
    galaxy_map = parse_map(file.read())

    # Expand the universe
    expanded_map = expand_universe(galaxy_map)
    # Identify galaxies and store their coordinates
    galaxies = identify_galaxies(expanded_map)
    # Calculate the sum of distances between all pairs of galaxies
    sum_of_distances = calculate_distances(galaxies)


    # Identify galaxies and store their coordinates in the original map
    galaxies_original = identify_galaxies(galaxy_map)
    # Scaling factor is 1 million
    scaling_factor = 1000000
    # Scale the coordinates of each galaxy
    scaled_galaxies = get_scaled_coordinates(galaxies_original, galaxy_map, scaling_factor)
    # Calculate the sum of distances between all pairs of galaxies using scaled coordinates
    scaled_sum_of_distances = calculate_distances(scaled_galaxies)


    print("First puzzle solution:", sum_of_distances)
    print("Second puzzle solution:", scaled_sum_of_distances)