"""
With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.
There's just one problem: you don't see any lava.
You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?
As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.
You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.
In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><
123456789

In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:
1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7

This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.
To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.
Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

Your puzzle answer was 34889.

--- Part Two ---
You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully nobody was watching, because that must have been pretty embarrassing.
Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or # should be the opposite type.
In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid. (The old reflection line won't necessarily continue being valid after the smudge is fixed.)

Here's the above example again:
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would have a different, horizontal line of reflection:
1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:
1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7

Now, the pattern has a different horizontal line of reflection between rows 1 and 2.
Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.
In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the new reflection line in each pattern in your notes?

Your puzzle answer was 34224.
"""

def is_vertical_reflection(pattern, col):
    """
    Check if there is a vertical reflection at the given column.
    """
    num_rows = len(pattern)
    num_cols = len(pattern[0])

    for row in range(num_rows):
        left = col
        right = col + 1
        while left >= 0 and right < num_cols:
            if pattern[row][left] != pattern[row][right]:
                return False
            left -= 1
            right += 1

    return True

def is_horizontal_reflection(pattern, row):
    """
    Check if there is a horizontal reflection at the given row.
    """
    num_rows = len(pattern)
    num_cols = len(pattern[0])

    for col in range(num_cols):
        top = row
        bottom = row + 1
        while top >= 0 and bottom < num_rows:
            if pattern[top][col] != pattern[bottom][col]:
                return False
            top -= 1
            bottom += 1

    return True

def find_reflection_line(pattern, original_reflection_line=None):
    """
    Find the reflection line in the pattern.
    """
    num_rows = len(pattern)
    num_cols = len(pattern[0])

    for col in range(num_cols - 1):
        if is_vertical_reflection(pattern, col):
            if original_reflection_line is not None and original_reflection_line[0] == 'vertical' and original_reflection_line[1] == col:
                continue
            return ('vertical', col)


    # Check for horizontal reflection
    for row in range(num_rows - 1):
        if is_horizontal_reflection(pattern, row):
            if original_reflection_line is not None and original_reflection_line[0] == 'horizontal' and original_reflection_line[1] == row:
                continue
            return ('horizontal', row)

    # No reflection found
    return (None, None)


def calculate_summary_number(reflection_lines):
    """
    Calculate the summary number based on the reflection lines.
    """
    total = 0
    for reflection_type, line_index in reflection_lines:
        if reflection_type == 'vertical':
            total += line_index + 1
        elif reflection_type == 'horizontal':
            total += 100 * (line_index + 1)
    return total

def get_patterns(input_lines):
    """
    Extracts individual patterns from the input lines.
    """
    patterns = []
    current_pattern = []

    for line in input_lines:
        line = line.strip()
        if line:
            current_pattern.append(line)
        else:
            if current_pattern:
                patterns.append(current_pattern)
                current_pattern = []

    # Add the last pattern if not empty
    if current_pattern:
        patterns.append(current_pattern)

    return patterns

def flip_character(char):
    """
    Flips the character from '.' to '#' or vice versa.
    """
    return '#' if char == '.' else '.'

def find_smudge_and_fix(pattern):
    """
    Locate the smudge in the pattern and determine the new, different reflection line.
    This involves iterating over rows and columns to find a flip that results in a different reflection.
    """
    num_rows = len(pattern)
    num_cols = len(pattern[0])

    original_reflection_line = find_reflection_line(pattern)

    for row in range(num_rows):
        for col in range(num_cols):
            # Flip one character at a time
            modified_pattern = [list(r) for r in pattern]
            modified_pattern[row][col] = flip_character(modified_pattern[row][col])

            new_reflection_line = find_reflection_line([''.join(r) for r in modified_pattern], original_reflection_line)

            # Check if the new reflection line is different from the original and valid
            if new_reflection_line[0] is not None and new_reflection_line != original_reflection_line:
                return new_reflection_line

    return original_reflection_line  # Return the original if no new line is found


with open('input.txt', 'r') as file:
    input_data = file.readlines()
    patterns = get_patterns(input_data)

    # Finding the reflection lines for each pattern
    reflection_lines = [find_reflection_line(pattern) for pattern in patterns]
    # Calculating the summary number for each pattern
    summary_number = calculate_summary_number(reflection_lines)

    # Finding the new reflection lines with the smudge fixed for each pattern
    new_reflection_lines_with_smudge = [find_smudge_and_fix(pattern) for pattern in patterns]
    # Calculating the summary number for the modified patterns
    summary_number_with_new_reflection = calculate_summary_number(new_reflection_lines_with_smudge)

    print("First puzzle solution: ", summary_number)
    print("Second puzzle solution: ", summary_number_with_new_reflection)

