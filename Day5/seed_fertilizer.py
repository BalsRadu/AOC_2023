"""
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.
"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.
"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.
"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"
You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.
The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.
Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.
Consider again the example seed-to-soil map:
50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.
The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.
Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.
So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:
Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:
Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

Your puzzle answer was 910845529.

--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.
The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:
seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.
Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.
In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.
Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

Your puzzle answer was 77435348.
"""
def parse_mappings(content):
    """
    Parses the provided content to extract seed numbers and the mappings for each category.
    Returns a dictionary with keys as category names and values as lists of mapping tuples.
    """
    mappings = {}
    seeds = []
    current_category = None
    for line in content:
        line = line.strip()
        if not line:
            continue

        if line.startswith('seeds:'):
            seeds = [int(seed) for seed in line.split(' ')[1:]]
        elif line.endswith('map:'):
            current_category = line[:-5]
            mappings[current_category] = []
        else:
            mapping = tuple(map(int, line.split(' ')))
            mappings[current_category].append(mapping)

    return seeds, mappings

def map_number(number, mapping_rules):
    """
    Maps a number through the given mapping rules.
    The rules are a list of tuples (destination_start, source_start, range_length).
    If a number does not fall within any source range, it maps to itself.
    """
    for destination_start, source_start, range_length in mapping_rules:
        if source_start <= number < source_start + range_length:
            return destination_start + (number - source_start)
    return number

def find_lowest_location(seeds, mappings):
    """
    Finds the lowest location number that corresponds to any of the initial seed numbers.
    Maps each seed number through the different categories to find its corresponding location number.
    """
    lowest_location = float('inf')

    for seed in seeds:
        location = seed
        for map in mappings:
            location = map_number(location, mappings[map])
        lowest_location = min(lowest_location, location)

    return lowest_location

def map_intervals(interval, mapping_rules):
    """
    Maps an interval of numbers through the given mapping rules.
    The rules are a list of tuples (destination_start, source_start, range_length).
    Returns a list of intervals resulting from the mapping.
    """
    result_intervals = []
    start, end = interval

    for destination_start, source_start, range_length in mapping_rules:
        source_end = source_start + range_length - 1
        interval_adjustment = destination_start - source_start

        # Case 1: Interval starts before and intersects with the mapping rule
        if start < source_start < end:
            if end <= source_end:
                result_intervals.append((start, source_start))  # Part before the mapping
                result_intervals.append((destination_start, destination_start + (end - source_start)))  # Mapped part
                return result_intervals  # Entire interval processed
            else:
                result_intervals.append((start, source_start))  # Part before the mapping
                start = source_end  # Adjust start for next mapping

        # Case 2: Interval is entirely within a mapping rule
        elif source_start <= start and end <= source_end:
            mapped_start = start + interval_adjustment
            mapped_end = end + interval_adjustment
            result_intervals.append((mapped_start, mapped_end))
            return result_intervals  # Entire interval processed

        # Case 3: Interval starts within a mapping rule but extends beyond it
        elif source_start <= start < source_end:
            mapped_start = start + interval_adjustment
            mapped_end = source_end + interval_adjustment
            result_intervals.append((mapped_start, mapped_end))  # Mapped part
            start = source_end + 1  # Adjust start for next mapping

    # Remaining part of the interval, if any, maps to itself
    if start <= end:
        result_intervals.append((start, end))

    return result_intervals

def find_lowest_location_intervals(seeds, mappings):
    """
    Finds the lowest location number that corresponds to any seed number in the seed intervals.
    """
    intervals = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for category in mappings:
        new_intervals = []
        for interval in intervals:
            mapped_intervals = map_intervals(interval, mappings[category])
            new_intervals.extend(mapped_intervals)
        intervals = new_intervals

    # Finding the lowest location number from the intervals
    return min(interval[0] for interval in intervals)

with open("input.txt") as file:
    lines = file.readlines()

    seeds, mappings = parse_mappings(lines)
    mappings = {k: sorted(v, key=lambda x: x[1]) for k, v in mappings.items()} # Sorted mappings by source start

    lowest_location_number = find_lowest_location(seeds, mappings)
    lowest_location_number_intervals = find_lowest_location_intervals(seeds, mappings)

    print("First puzzle solution:", lowest_location_number)
    print("Second puzzle solution:", lowest_location_number_intervals)