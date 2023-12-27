"""
The Elves resume water filtering operations! Clean water starts flowing over the edge of Island Island.

They offer to help you go over the edge of Island Island, too! Just hold on tight to one end of this impossibly long rope and they'll lower you down a safe distance from the massive waterfall you just created.

As you finally reach Snow Island, you see that the water isn't really reaching the ground: it's being absorbed by the air itself. It looks like you'll finally have a little downtime while the moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow; why not take a walk?

There's a map of nearby hiking trails (your puzzle input) that indicates paths (.), forest (#), and steep slopes (^, >, v, and <).

For example:

#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
You're currently on the single path tile in the top row; your goal is to reach the single path tile in the bottom row. Because of all the mist from the waterfall, the slopes are probably quite icy; if you step onto a slope tile, your next step must be downhill (in the direction the arrow is pointing). To make sure you have the most scenic hike possible, never step onto the same tile twice. What is the longest hike you can take?

In the example above, the longest hike you can take is marked with O, and your starting position is marked S:

#S#####################
#OOOOOOO#########...###
#######O#########.#.###
###OOOOO#OOO>.###.#.###
###O#####O#O#.###.#.###
###OOOOO#O#O#.....#...#
###v###O#O#O#########.#
###...#O#O#OOOOOOO#...#
#####.#O#O#######O#.###
#.....#O#O#OOOOOOO#...#
#.#####O#O#O#########v#
#.#...#OOO#OOO###OOOOO#
#.#.#v#######O###O###O#
#...#.>.#...>OOO#O###O#
#####v#.#.###v#O#O###O#
#.....#...#...#O#O#OOO#
#.#########.###O#O#O###
#...###...#...#OOO#O###
###.###.#.###v#####O###
#...#...#.#.>.>.#.>O###
#.###.###.#.###.#.#O###
#.....###...###...#OOO#
#####################O#
This hike contains 94 steps. (The other possible hikes you could have taken were 90, 86, 82, 82, and 74 steps long.)

Find the longest hike you can take through the hiking trails listed on your map. How many steps long is the longest hike?

Your puzzle answer was 2358.

--- Part Two ---
As you reach the trailhead, you realize that the ground isn't as slippery as you expected; you'll have no problem climbing up the steep slopes.

Now, treat all slopes as if they were normal paths (.). You still want to make sure you have the most scenic hike possible, so continue to ensure that you never step onto the same tile twice. What is the longest hike you can take?

In the example above, this increases the longest hike to 154 steps:

#S#####################
#OOOOOOO#########OOO###
#######O#########O#O###
###OOOOO#.>OOO###O#O###
###O#####.#O#O###O#O###
###O>...#.#O#OOOOO#OOO#
###O###.#.#O#########O#
###OOO#.#.#OOOOOOO#OOO#
#####O#.#.#######O#O###
#OOOOO#.#.#OOOOOOO#OOO#
#O#####.#.#O#########O#
#O#OOO#...#OOO###...>O#
#O#O#O#######O###.###O#
#OOO#O>.#...>O>.#.###O#
#####O#.#.###O#.#.###O#
#OOOOO#...#OOO#.#.#OOO#
#O#########O###.#.#O###
#OOO###OOO#OOO#...#O###
###O###O#O###O#####O###
#OOO#OOO#O#OOO>.#.>O###
#O###O###O#O###.#.#O###
#OOOOO###OOO###...#OOO#
#####################O#
Find the longest hike you can take through the surprisingly dry hiking trails listed on your map. How many steps long is the longest hike?

Your puzzle answer was 6586.
"""
from collections import defaultdict

def create_graph(map_data):
    """
    Convert the map data into a graph where each node represents a tile (path or slope),
    and edges represent possible movements according to the map rules.
    """
    graph = defaultdict(dict)
    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

    for i, row in enumerate(map_data):
        for j, tile in enumerate(row):
            if tile in '.^>v<':
                for di, dj in [directions[tile]] if tile in directions else directions.values():
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(map_data) and 0 <= nj < len(map_data[ni]) and map_data[ni][nj] in '.^>v<':
                        graph[(i, j)][(ni, nj)] = 1

    return graph

def create_intersection_graph(map_data):
    """
    Convert the map data into a graph where nodes are intersections and dead ends.
    Edges represent paths between these nodes with their length as weights.
    """
    graph = defaultdict(dict)
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def is_open_tile(tile):
        return tile in '.^>v<'

    def is_intersection_or_dead_end(i, j):
        open_neighbors = sum(is_open_tile(map_data[i + di][j + dj])
                             for di, dj in directions
                             if 0 <= i + di < len(map_data) and 0 <= j + dj < len(map_data[0]))
        return open_neighbors > 2 or open_neighbors == 1

    def bfs(start, end):
        """ Breadth-first search to find the shortest path from start to end and its length """
        queue = [(start, [start])]
        visited = {start}

        while queue:
            current, path = queue.pop(0)
            if current == end:
                return len(path) - 1

            for di, dj in directions:
                ni, nj = current[0] + di, current[1] + dj
                if (0 <= ni < len(map_data) and 0 <= nj < len(map_data[0]) and
                is_open_tile(map_data[ni][nj]) and (ni, nj) not in visited):
                     if (ni, nj) == end or not is_intersection_or_dead_end(ni, nj):
                        visited.add((ni, nj))
                        queue.append(((ni, nj), path + [(ni, nj)]))

        return 0  # No path found

    # Identify all intersections and dead ends as nodes
    nodes = [(i, j) for i in range(len(map_data)) for j in range(len(map_data[0])) if is_open_tile(map_data[i][j]) and is_intersection_or_dead_end(i, j)]

    # Find paths between nodes
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            length = bfs(nodes[i], nodes[j])
            if length:
                graph[nodes[i]][nodes[j]] = length
                graph[nodes[j]][nodes[i]] = length  # Graph is undirected

    return graph

def dfs(graph, start_node, end_node):
    """ Depth-first search to find the longest path from start to end and its length """
    stack = [(start_node, set([start_node]), 0)]
    longest_path = 0
    longest_path_count = 0
    stop_count = 10 ** 5

    while stack:
        current_node, visited, path_length = stack.pop()
        if current_node == end_node:

            if path_length > longest_path:
                longest_path = path_length
                longest_path_count = 1

            if longest_path_count > stop_count:
                 break

            longest_path_count += 1

        else:
            for neighbor, length in graph[current_node].items():
                if neighbor not in visited:
                    new_visited = visited.copy()
                    new_visited.add(neighbor)
                    stack.append((neighbor, new_visited, path_length + length))

    return longest_path

with open('input.txt', 'r') as f:
    content = f.read().strip()
    # Parse the map from the file content
    map_data = [list(row) for row in content.split('\n')]

    # Display the size of the map and a small portion to verify the parsing
    map_height = len(map_data)
    map_width = len(map_data[0]) if map_height > 0 else 0

    # # Create the graph from the map data
    graph = create_graph(map_data)

    # Find the start and end nodes (single path tile in the top and bottom rows)
    start_node = next((i, j) for i in range(map_height) for j in range(map_width) if map_data[i][j] == '.' and i == 0)
    end_node = next((i, j) for i in range(map_height) for j in range(map_width) if map_data[i][j] == '.' and i == map_height - 1)

    # Perform the DFS search to find the longest path for the first part of the puzzle
    longest_path_length = dfs(graph, start_node, end_node)

    # Create the intersection graph from the map data
    intersection_graph = create_intersection_graph(map_data)

    # Perform the DFS search to find the longest path for the second part of the puzzle
    longest_path_length_no_slopes = dfs(intersection_graph, start_node, end_node)

    print("First puzzle solution:", longest_path_length)
    print("Second puzzle solution:", longest_path_length_no_slopes)


