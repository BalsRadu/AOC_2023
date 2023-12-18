import heapq
import numpy as np


def parse_input(input_str):
    """Parse the input string into a 2D numpy array."""
    grid_lines = input_str.strip().split('\n')
    grid = np.array([list(map(int, line)) for line in grid_lines])
    return grid

def find_min_heat_loss(grid):
    """Find the path with the minimum heat loss using BFS with a priority queue."""
    rows, cols = grid.shape
    # Initialize a 4D array to store the minimum heat loss at each position with a direction and steps
    min_loss = np.full((rows, cols, 4, 3), np.inf)  # 4 directions, 3 steps

    # Direction vectors: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # Priority queue for BFS: elements are tuples (total_loss, row, col, direction, steps)
    pq = [(0, 0, 0, d, 0) for d in range(4)]  # Start from (0, 0) in all directions

    while pq:
        loss, r, c, d, steps = heapq.heappop(pq)

        # Check bounds
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue

        # Calculate heat loss for the current cell
        new_loss = loss + grid[r, c] if (r, c) != (0, 0) else 0  # Exclude the starting cell's heat loss

        # Update the minimum loss for the current cell and direction
        if new_loss < min_loss[r, c, d, steps]:
            min_loss[r, c, d, steps] = new_loss
        else:
            continue  # Skip if we've already found a better path

        # Check if we reached the destination
        if (r, c) == (rows - 1, cols - 1):
            continue

        # Continue in the same direction if not exceeded the step limit
        if steps < 2:
            dr, dc = directions[d]
            heapq.heappush(pq, (new_loss, r + dr, c + dc, d, steps + 1))

        # Turn left and right
        for turn in [-1, 1]:
            new_d = (d + turn) % 4
            dr, dc = directions[new_d]
            heapq.heappush(pq, (new_loss, r + dr, c + dc, new_d, 0))

    # The minimum heat loss to the destination
    return min(min_loss[rows - 1, cols - 1, :, 0])


with open('input.txt', 'r') as file:
    input_data = file.read()
    grid = parse_input(input_data)

    min_heat_loss = find_min_heat_loss(grid)

    print("First puzzle solution is: ", min_heat_loss)
