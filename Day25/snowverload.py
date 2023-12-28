from functools import lru_cache
from itertools import combinations, tee
import random
from collections import Counter
import networkx as nx

def parse_input(input_data):
    """
    Parses the input data to construct a graph.
    The function reads the input data line by line. Each line represents a node and its directly connected nodes
    in the format 'node: connected_node1 connected_node2 ...'. It constructs and returns a graph where each node is
    connected to its corresponding nodes.
    """

    graph = nx.Graph()

    for line in input_data.strip().split("\n"):
        parts = line.split(": ")
        node = parts[0]
        connected_nodes = parts[1].split()
        for connected_node in connected_nodes:
            graph.add_edge(node, connected_node)
    return graph

@lru_cache(maxsize=None)
def descendants_at_distance_one(graph, node):
    """
    Returns the descendants of a node at a distance of one in the graph.

    This function is memoized using lru_cache to improve performance by caching the results of previous calls.
    It uses NetworkX's descendants_at_distance function to get all nodes that are exactly one edge away
    from the specified node.
    """
    return nx.descendants_at_distance(graph, node, 1)

def pairwise(iterable):
    """
    Generates pairs of adjacent elements from the input iterable.

    This function is a utility to create a pairwise combination of elements from an iterable. For example,
    given [1, 2, 3], it yields (1, 2), (2, 3). It's used to iterate over edges in a path represented as a
    sequence of nodes.
    """
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def find_optimal_cuts(graph, num_cuts=3):
    """
    Finds the optimal set of edges to cut in the graph to split it into two approximately equal parts.

    The algorithm first identifies cut candidates - edges whose removal doesn't result in immediate smaller
    fragments. It then samples random paths in the graph, tallying the frequency of each candidate edge in these
    paths. The idea is that edges appearing frequently in random paths are more likely to split the graph
    into large, approximately equal parts when cut. The top edges based on this frequency count are then
    chosen as cuts. The graph is split by these cuts, and the product of the sizes of the resulting two
    largest components is calculated.
    """
    # Finding nodes and preparing cut candidates
    nodes = list(graph)
    cut_candidates = {
        frozenset((a, b)) for (a, b) in combinations(graph, 2) if b in descendants_at_distance_one(graph, a)
        and not (descendants_at_distance_one(graph, a) & descendants_at_distance_one(graph, b))
    }

    # Sampling paths and counting edges in cut candidates
    edge_counts = Counter()
    for _ in range(1000):
        for edge in pairwise(nx.shortest_path(graph, *random.choices(nodes, k=2))):
            edgefs = frozenset(edge)
            if edgefs in cut_candidates:
                edge_counts[edgefs] += 1

    # Selecting top edges to cut
    top_edges = [tuple(edgefs) for (edgefs, count) in edge_counts.most_common(num_cuts)]

    # Removing selected edges and calculating the product of the sizes of the two components
    temp_graph = graph.copy()
    temp_graph.remove_edges_from(top_edges)
    components = list(nx.connected_components(temp_graph))
    if len(components) == 2:
        return len(components[0]) * len(components[1])
    else:
        return None

# Read the input data
with open("input.txt", 'r') as file:
    input_data = file.read()

# Parsing the input data into a graph
graph = parse_input(input_data)

# Finding the optimal cuts
product = find_optimal_cuts(graph)

print("First puzzle solution:", product)