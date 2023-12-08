"""
You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.
One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.
It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!
After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually.

For example:
RL
AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.
Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:
LLR
AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

Your puzzle answer was 16043.

--- Part Two ---
The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!
What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.
After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:
LR
11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:
Step 0: You are at 11A and 22A.
Step 1: You choose all of the left paths, leading you to 11B and 22B.
Step 2: You choose all of the right paths, leading you to 11Z and 22C.
Step 3: You choose all of the left paths, leading you to 11B and 22Z.
Step 4: You choose all of the right paths, leading you to 11Z and 22B.
Step 5: You choose all of the left paths, leading you to 11B and 22C.
Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

Your puzzle answer was 15726453850399.
"""
from math import gcd
from functools import reduce

# Function to navigate through the nodes
def navigate_to_zzz(start_node, instructions, nodes):
    current_node = start_node
    steps = 0
    instruction_index = 0

    while current_node != 'ZZZ':
        # Get the next instruction and update the index
        instruction = instructions[instruction_index]
        instruction_index = (instruction_index + 1) % len(instructions)

        # Navigate to the next node
        if instruction == 'L':
            current_node = nodes[current_node][0]
        else:  # 'R'
            current_node = nodes[current_node][1]

        steps += 1

    return steps


def already_found(destination_nodes, node):
    for destination in destination_nodes:
        if destination[0] == node:
            return True
    return False


# Function to navigate through the network from each start node
def navigate(start_node, instructions, nodes):
        current_node = start_node
        steps = 0
        instruction_index = 0
        visited = {current_node: 0}  # Tracks visited nodes and their positions in the instruction sequence
        destination_nodes = []  # List of destination nodes found

        while True:
            # Get the next instruction and update the index
            instruction = instructions[instruction_index]
            instruction_index = (instruction_index + 1) % len(instructions)

            # Navigate to the next node
            if instruction == 'L':
                current_node = nodes[current_node][0]
            else:  # 'R'
                current_node = nodes[current_node][1]

            steps += 1

            # Check for a destination node and add to the list
            if current_node.endswith('Z') and not already_found(destination_nodes, current_node):
                destination_nodes.append((current_node, steps))

            # Check for end conditions: loop or node pointing to itself
            if (current_node in visited and visited[current_node] == instruction_index) or \
               (nodes[current_node][0] == current_node and nodes[current_node][1] == current_node):
                return destination_nodes

            # Update visited nodes
            visited[current_node] = instruction_index

def find_paths_to_destination_nodes(start_node, instructions, nodes):
    # Applying the function to each start node
    results = {}
    for start_node in start_nodes:
        destinations = navigate(start_node, instructions, nodes)
        results[start_node] = destinations

    return results

# Function to find the least common multiple (LCM) of a list of numbers
def lcm(numbers):
    def lcm_of_two(a, b):
        return a * b // gcd(a, b)
    return reduce(lcm_of_two, numbers, 1)

# Open the input file and read the lines
with open("input.txt") as file:
    lines = file.readlines()

    # Separating the instructions and the node definitions
    instructions = lines[0].strip()  # The first line contains the instructions
    node_definitions = lines[2:]  # Skip the first two lines (instructions and an empty line)

    # Parsing node definitions
    nodes = {}
    for line in node_definitions:
        parts = line.strip().split(' = ')
        node_label = parts[0]
        left_right = parts[1].strip('()').split(', ')
        nodes[node_label] = left_right

    # Calculate the number of steps to reach 'ZZZ'
    steps_to_zzz = navigate_to_zzz('AAA', instructions, nodes)

    # Collecting the start nodes (nodes ending with 'A')
    start_nodes = [node for node in nodes if node.endswith('A')]

    # Finding the destination nodes for each start node
    all_destinations_results = find_paths_to_destination_nodes(start_nodes, instructions, nodes)

    # Extracting the number of steps for each start node
    steps_list = [all_destinations_results[node][0][-1] for node in all_destinations_results]

    # Calculating the least multiple where all nodes end up in a destination node
    ghost_steps = lcm(steps_list)

    print("First puzzle solution:", steps_to_zzz)
    print("Second puzzle solution:", ghost_steps)

