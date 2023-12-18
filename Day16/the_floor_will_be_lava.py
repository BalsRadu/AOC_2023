def simulate_beam(grid):
    rows = len(grid)
    cols = len(grid[0].strip())  # Removing potential newline characters
    energized_tiles = set()  # Using a set to avoid duplicates

    def traverse(x, y, dx, dy):
        while 0 <= x < cols and 0 <= y < rows:
            if (x, y, dx, dy) in energized_tiles:
                # If the beam returns to a previously energized tile with the same direction, stop to avoid infinite loops
                break

            energized_tiles.add((x, y, dx, dy))

            current_tile = grid[y][x]

            if current_tile == '.':
                # Continue in the same direction
                x += dx
                y += dy
            elif current_tile == '/':
                # Reflect the beam
                dx, dy = -dy, -dx
                x += dx
                y += dy
            elif current_tile == '\\':
                # Reflect the beam
                dx, dy = dy, dx
                x += dx
                y += dy
            elif current_tile in '|-':
                if (dx == 0 and current_tile == '|') or (dy == 0 and current_tile == '-'):
                    # Beam passes through the pointy end of a splitter
                    x += dx
                    y += dy
                else:
                    # Split the beam
                    traverse(x, y, -dy, dx)  # Reflect horizontally
                    traverse(x, y, dy, -dx)  # Reflect vertically
                    break

    # Start the simulation from top-left corner, heading right
    traverse(0, 0, 1, 0)

    # Count unique tiles that were energized, regardless of the direction of the beam
    unique_tiles_energized = {tile[:2] for tile in energized_tiles}
    return len(unique_tiles_energized)

def find_specific_max_energized_tiles(grid):
    rows = len(grid)
    cols = len(grid[0].strip())
    max_energized = 0
    best_start = None

    # Define the starting points and directions for the beam on all edges
    starting_points = [(0, i, 0, 1) for i in range(cols)] + \
                      [(rows - 1, i, 0, -1) for i in range(cols)] + \
                      [(i, 0, 1, 0) for i in range(rows)] + \
                      [(i, cols - 1, -1, 0) for i in range(rows)]

    for y, x, dx, dy in starting_points:
        energized_tiles = set()

        def traverse(x, y, dx, dy):
            while 0 <= x < cols and 0 <= y < rows:
                if (x, y, dx, dy) in energized_tiles:
                    break

                energized_tiles.add((x, y, dx, dy))

                current_tile = grid[y][x]

                if current_tile == '.':
                    x += dx
                    y += dy
                elif current_tile == '/':
                    dx, dy = -dy, -dx
                    x += dx
                    y += dy
                elif current_tile == '\\':
                    dx, dy = dy, dx
                    x += dx
                    y += dy
                elif current_tile in '|-':
                    if (dx == 0 and current_tile == '|') or (dy == 0 and current_tile == '-'):
                        x += dx
                        y += dy
                    else:
                        traverse(x, y, -dy, dx)
                        traverse(x, y, dy, -dx)
                        break

        traverse(x, y, dx, dy)

        unique_tiles_energized = {tile[:2] for tile in energized_tiles}
        energized_count = len(unique_tiles_energized)
        if energized_count > max_energized:
            max_energized = energized_count

    return max_energized

with open('input.txt') as f:
    grid_input = f.readlines()

    # Applying the simulation on the input grid
    energized_tiles_count = simulate_beam(grid_input)
    # Applying the simulation on the input grid, but starting from all edges
    max_energized_tiles = find_specific_max_energized_tiles(grid_input)


    print("First puzzle solution:", energized_tiles_count)
    print("Second puzzle solution:", max_energized_tiles)