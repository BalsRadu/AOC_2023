"""
You finally reach the hot springs! You can see steam rising from secluded areas attached to the primary, ornate building.
As you turn to enter, the researcher stops you. "Wait - I thought you were looking for the hot springs, weren't you?" You indicate that this definitely looks like hot springs to you.
"Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."
You look in the direction the researcher is pointing and suddenly notice the massive metal helixes towering overhead. "This way!"
It only takes you a few more steps to reach the main gate of the massive fenced-off area containing the springs. You go through the gate and into a small administrative building.
"Hello! What brings you to the hot springs today? Sorry they're not very hot right now; we're having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.
"Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, not until we get more lava to heat our forges. And our springs. The springs aren't very springy unless they're hot!"
"Say, could you go up and see why the lava stopped flowing? The springs are too cold for normal operation, but we should be able to find one springy enough to launch you up there!"
There's just one problem - many of the springs have fallen into disrepair, so they're not actually sure which springs would even be safe to use! Worse yet, their condition records of which springs are damaged (your puzzle input) are also damaged! You'll need to help them repair the damaged records.
In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.
However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:
#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1

However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,

Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.
In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.
The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.
The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:

?###???????? 3,2,1
.###.##.#...
.###.##..#..
.###.##...#.
.###.##....#
.###..##.#..
.###..##..#.
.###..##...#
.###...##.#.
.###...##..#
.###....##.#

In this example, the number of possible arrangements for each row is:
???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 4 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 1 arrangement
????.######..#####. 1,6,5 - 4 arrangements
?###???????? 3,2,1 - 10 arrangements

Adding all of the possible arrangement counts together produces a total of 21 arrangements.
For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?

Your puzzle answer was 7541.

--- Part Two ---
As you look out at the field of springs, you feel like there are way more springs than the condition records list. When you examine the records, you discover that they were actually folded up this whole time!
To unfold the records, on each row, replace the list of spring conditions with five copies of itself (separated by ?) and replace the list of contiguous groups of damaged springs with five copies of itself (separated by ,).

So, this row:
.#

Would become:
.#?.#?.#?.#?.# 1,1,1,1,1

The first line of the above example would become:
???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3

In the above example, after unfolding, the number of possible arrangements for some rows is now much larger:
???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 16384 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 16 arrangements
????.######..#####. 1,6,5 - 2500 arrangements
?###???????? 3,2,1 - 506250 arrangements

After unfolding, adding all of the possible arrangement counts together produces 525152.
Unfold your condition records; what is the new sum of possible arrangement counts?

Your puzzle answer was 17485169859432.
"""
# Define constants for the different spring conditions
EMPTY = '.'
SPRING = '#'
UNKNOWN = '?'

def parse_input(line, unfold=False):
    """
    Parse a single line of the input file and optionally unfold it.
    """
    parts = line.strip().split(' ')
    springs = parts[0]
    groups = parts[1]

    if unfold:
        springs = ('?' + springs) * 5
        springs = springs[1:]  # Remove the leading '?'
        groups = ','.join([groups for _ in range(5)])

    return [x for x in springs], [int(x) for x in groups.split(',') if x]

def count_arrangements(springs, groups):
    """
    Count the number of valid arrangements of springs based on the input line.

    The algorithm works as follows:
    - A recursive function, `recursive_count`, explores all possible arrangements.
      It tries to place each group of springs in sequence, considering the constraints.
    - A dynamic programming approach is used via a cache (`cache`) to store and reuse the results of subproblems.
    - The algorithm also calculates the required space for each group, which aids in pruning the search space.
    - The base case of the recursion is when all groups are placed. In this case, the function checks if the remaining positions can all be empty.
    - If there's not enough space for the remaining groups, the branch is abandoned (returns 0).
    - The function explores two possibilities at each step:
      1. Placing the current group at the current index, if conditions allow.
      2. Skipping the current position (considering it empty) and trying the next one.
      """
    # Cache for memoization to optimize recursive calls
    cache = {}

    # Calculate the required space for each group
    required_space = [0] * len(groups)
    space = 0
    for i in range(len(groups) - 1, -1, -1):
        space += groups[i]
        required_space[i] = space
        space += 1  # Adding space for the gap between groups

    def recursive_count(index, group):
        # Check the cache to avoid recalculating known results
        if (index, group) in cache:
            return cache[(index, group)]

        # Base case: If all groups have been placed, check if the remaining springs can all be empty
        if group == len(groups):
            return 1 if all(cond != SPRING for cond in springs[index:]) else 0

        # If there's not enough space left for the remaining groups, return 0
        if index + required_space[group] > len(springs):
            return 0

        sum_arrangements = 0  # Initialize the sum of valid arrangements
        group_value = groups[group]
        next_index = index + group_value + 1

        # Check if a group can be placed at the current index
        if not (0 <= index + group_value < len(springs) and springs[index + group_value] == SPRING) and \
           all(cond != EMPTY for cond in springs[index:index + group_value]):
            sum_arrangements += recursive_count(next_index, group + 1)


        # Check if the current position can be left empty and continue the recursion
        if springs[index] != SPRING:
            sum_arrangements += recursive_count(index + 1, group)

        # Store the result in the cache and return it
        cache[(index, group)] = sum_arrangements
        return sum_arrangements

    # Start the recursive process from the beginning
    return recursive_count(0, 0)


with open('input.txt') as file:
    lines = file.readlines()

    # Part One: Count arrangements without unfolding
    arrangement_counts_part_one = sum([count_arrangements(*parse_input(line)) for line in lines])
    print("Part One solution:", arrangement_counts_part_one)

    # Part Two: Count arrangements with unfolding
    arrangement_counts_part_two = sum([count_arrangements(*parse_input(line, unfold=True)) for line in lines])
    print("Part Two solution:", arrangement_counts_part_two)