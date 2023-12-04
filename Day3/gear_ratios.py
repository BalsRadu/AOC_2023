"""
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.
It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.
"Aaah!"
You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

Your puzzle answer was 540212.

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.
You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.
Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
What is the sum of all of the gear ratios in your engine schematic?

Your puzzle answer was 87605697.
"""

def is_symbol(char):
    """Check if the character is a symbol (not a period or a digit)."""
    return not (char.isdigit() or char == '.')

def sum_part_numbers(schematic):
    """Calculate the sum of all part numbers in the engine schematic with symbol-based number identification."""
    sum_of_parts = 0
    num_rows = len(schematic)

    for row in range(num_rows):
        line = schematic[row].strip()  # Remove newline characters
        num_cols = len(line)
        col = 0

        while col < num_cols:
            if line[col].isdigit():
                # Found the start of a number, now find its end
                start_index = col
                while col < num_cols and line[col].isdigit():
                    col += 1
                end_index = col - 1

                # Define the rectangle around the number with additional line checks
                top = max(0, row - 1)
                bottom = min(num_rows - 1, row + 1)
                left = max(0, start_index - 1)
                right = min(num_cols - 1, end_index + 1)

                # Check surroundings for symbols
                has_symbol = False
                for r in range(top, bottom + 1):
                    for c in range(left, right + 1):
                        if r == row and c >= start_index and c <= end_index:
                            continue  # Skip the number itself
                        if is_symbol(schematic[r][c]):
                            has_symbol = True
                            break
                    if has_symbol:
                        break

                # Additionally, check the immediate left and right on the same line
                if not has_symbol:
                    if start_index > 0 and is_symbol(line[start_index - 1]):
                        has_symbol = True
                    elif end_index < num_cols - 1 and is_symbol(line[end_index + 1]):
                        has_symbol = True

                # Add the number to the sum if a symbol is found
                if has_symbol:
                    sum_of_parts += int(line[start_index:col])
            else:
                col += 1

    return sum_of_parts


def find_gears_and_calculate_ratios_with_position_check(schematic):
    """Find gears and calculate their ratios in the engine schematic with position-based number identification."""
    num_rows = len(schematic)
    gear_ratios_sum = 0

    for row in range(num_rows):
        line = schematic[row].strip()
        num_cols = len(line)

        for col in range(num_cols):
            if line[col] == '*':
                # Found a gear, now check its surroundings for part numbers
                top = max(0, row - 1)
                bottom = min(num_rows - 1, row + 1)
                left = max(0, col - 1)
                right = min(num_cols - 1, col + 1)

                part_numbers = []

                # Check surrounding including diagonals for part numbers
                for r in range(top, bottom + 1):
                    for c in range(left, right + 1):
                        if r == row and c == col:
                            continue  # Skip the gear itself

                        if schematic[r][c].isdigit():
                            # Found a digit, determine the boundaries of the number
                            start_index, end_index = c, c

                            # Determine the horizontal boundaries of the number
                            while start_index > 0 and schematic[r][start_index - 1].isdigit():
                                start_index -= 1
                            while end_index < num_cols - 1 and schematic[r][end_index + 1].isdigit():
                                end_index += 1

                            # Extract the number and its position
                            number = int(schematic[r][start_index:end_index + 1])
                            position = (r, start_index, end_index)

                            # Add the number with its position
                            if (number, position) not in part_numbers:
                                part_numbers.append((number, position))

                            # Break if two numbers are found
                            if len(part_numbers) == 2:
                                break
                    if len(part_numbers) == 2:
                        break

                # Calculate the gear ratio if exactly two part numbers are found
                if len(part_numbers) == 2:
                    gear_ratio = part_numbers[0][0] * part_numbers[1][0]
                    gear_ratios_sum += gear_ratio

    return gear_ratios_sum


with open("input.txt") as file:
    engine_schematic = file.readlines()

    # Calculate the sum of all the part numbers
    sum_of_parts = sum_part_numbers(engine_schematic)
    gear_ration_sum = find_gears_and_calculate_ratios_with_position_check(engine_schematic)

    print("First puzzle solution:", sum_of_parts)
    print("Second puzzle solution:", gear_ration_sum)


