def parse_layout(layout):
    """
    Parse the layout into a grid and return the grid and the starting position.
    """
    grid = [list(line) for line in layout.split('\n')]
    start_pos = None

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                start_pos = (x, y)
                break
        if start_pos:
            break

    return grid, start_pos


# Define the connections for each pipe type
connections = {
    '|': [(0, 1), (0, -1)],
    '-': [(1, 0), (-1, 0)],
    'L': [(1, 0), (0, -1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(-1, 0), (0, 1)],
    'F': [(1, 0), (0, 1)],
}

def infer_start_tile(grid, start_pos):
    """
    Infer the starting tile type from the connections of its neighbors.
    """
    x, y = start_pos
    for pipe_type, directions in connections.items():
        connected_neighbors = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] not in ['.', 'S']:
                neighbor_directions = connections.get(grid[ny][nx], [])
                if (-dx, -dy) in neighbor_directions:
                    connected_neighbors += 1
        # The correct tile type should connect to exactly two neighbors
        if connected_neighbors == 2:
            return pipe_type
    return None

def get_neighbors(pos, grid):
    """
    Get the neighbors of a given position that are part of the pipe.
    """
    x, y = pos
    neighbors = []

    # Check each direction
    for dx, dy in connections.get(grid[y][x], []):
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] in connections:
            neighbors.append((nx, ny))

    return neighbors


def find_loop_length(grid, start_pos, start_tile_type):
    """
    Find the length of the loop starting at the starting position.
    """

    # Replace 'S' with its inferred type for the traversal
    x, y = start_pos
    grid[y][x] = start_tile_type

    visited = set()
    to_visit = [(start_pos, 0)]
    max_distance = 0

    while to_visit:
        current_pos, distance = to_visit.pop(0)
        if current_pos in visited:
            continue

        visited.add(current_pos)
        max_distance = max(max_distance, distance)

        for neighbor in get_neighbors(current_pos, grid):
            if neighbor not in visited:
                to_visit.append((neighbor, distance + 1))

    return max_distance


def find_loop_boundaries(grid, start_pos, start_tile_type):
    """
    Find the boundaries of the loop and return them as a dictionary.
    """
    # Replace 'S' with its inferred type for traversal
    x, y = start_pos
    grid[y][x] = start_tile_type

    visited = set()
    to_visit = [(start_pos, 0)]
    boundaries = {}

    while to_visit:
        current_pos, _ = to_visit.pop(0)
        if current_pos in visited:
            continue

        visited.add(current_pos)
        x, y = current_pos

        # Add the X-coordinate to the list of boundaries for this Y-coordinate
        if y not in boundaries:
            boundaries[y] = []
        boundaries[y].append(x)

        for neighbor in get_neighbors(current_pos, grid):
            if neighbor not in visited:
                to_visit.append((neighbor, 0))

    # Sort the X-coordinates for each Y-coordinate
    for y in boundaries:
        boundaries[y].sort()

    return boundaries


def clean_layout(grid, boundaries):
    """
    Clean the layout to keep only the pipes that are part of the loop.
    """
    cleaned_grid = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for y in boundaries:
        for x in boundaries[y]:
            cleaned_grid[y][x] = grid[y][x]

    return cleaned_grid

def count_enclosed_tiles(grid):
    """
    Count the number of tiles enclosed within the loop.
    """
    enclosed_tiles = 0

    for row in grid:
        inside_loop = False
        for tile in row:
            if tile in ['|', 'L', 'J']:
                inside_loop = not inside_loop
            elif inside_loop and tile == '.':
                enclosed_tiles += 1

    return enclosed_tiles



with open("input.txt") as file:
    pipe_layout = file.read()

    # Parse the layout and find the loop length
    grid, start_pos = parse_layout(pipe_layout)
    # Infer the starting tile type
    start_tile_type = infer_start_tile(grid, start_pos)
    # Find the loop length
    loop_length = find_loop_length(grid, start_pos, start_tile_type)

    # Find the boundaries of the loop
    boundaries = find_loop_boundaries(grid, start_pos, start_tile_type)
    # Clean the layout to keep only the pipes that are part of the loop
    cleaned_grid = clean_layout(grid, boundaries)
    # Count the number of tiles enclosed within the loop
    enclosed_tiles = count_enclosed_tiles(cleaned_grid)

    print("First puzzle solution:", loop_length)
    print("Second puzzle solution:", enclosed_tiles)

