"""
--- Day 25: Snowverload ---
Still somehow without snow, you go to the last place you haven't checked: the center of Snow Island, directly below the waterfall.

Here, someone has clearly been trying to fix the problem. Scattered everywhere are hundreds of weather machines, almanacs, communication modules, hoof prints, machine parts, mirrors, lenses, and so on.

Somehow, everything has been wired together into a massive snow-producing apparatus, but nothing seems to be running. You check a tiny screen on one of the communication modules: Error 2023. It doesn't say what Error 2023 means, but it does have the phone number for a support line printed on it.

"Hi, you've reached Weather Machines And So On, Inc. How can I help you?" You explain the situation.

"Error 2023, you say? Why, that's a power overload error, of course! It means you have too many components plugged in. Try unplugging some components and--" You explain that there are hundreds of components here and you're in a bit of a hurry.

"Well, let's see how bad it is; do you see a big red reset button somewhere? It should be on its own module. If you push it, it probably won't fix anything, but it'll report how overloaded things are." After a minute or two, you find the reset button; it's so big that it takes two hands just to get enough leverage to push it. Its screen then displays:

SYSTEM OVERLOAD!

Connected components would require
power equal to at least 100 stars!
"Wait, how many components did you say are plugged in? With that much equipment, you could produce snow for an entire--" You disconnect the call.

You have nowhere near that many stars - you need to find a way to disconnect at least half of the equipment here, but it's already Christmas! You only have time to disconnect three wires.

Fortunately, someone left a wiring diagram (your puzzle input) that shows how the components are connected. For example:

jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
Each line shows the name of a component, a colon, and then a list of other components to which that component is connected. Connections aren't directional; abc: xyz and xyz: abc both represent the same configuration. Each connection between two components is represented only once, so some components might only ever appear on the left or right side of a colon.

In this example, if you disconnect the wire between hfx/pzl, the wire between bvb/cmg, and the wire between nvd/jqt, you will divide the components into two separate, disconnected groups:

9 components: cmg, frs, lhk, lsr, nvd, pzl, qnr, rsh, and rzs.
6 components: bvb, hfx, jqt, ntq, rhn, and xhk.
Multiplying the sizes of these groups together produces 54.

Find the three wires you need to disconnect in order to divide the components into two separate groups. What do you get if you multiply the sizes of these two groups together?

Your puzzle answer was 602151.

--- Part Two ---
You climb over weather machines, under giant springs, and narrowly avoid a pile of pipes as you find and disconnect the three wires.

A moment after you disconnect the last wire, the big red reset button module makes a small ding noise:

System overload resolved!
Power required is now 50 stars.
Out of the corner of your eye, you notice goggles and a loose-fitting hard hat peeking at you from behind an ultra crucible. You think you see a faint glow, but before you can investigate, you hear another small ding:

Power required is now 49 stars.

Please supply the necessary stars and
push the button to restart the system.
"""
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