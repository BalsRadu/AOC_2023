def parse_and_calculate_card_points(card_line):
    """
    Parse a card line to extract the winning and own numbers,
    and then calculate the points for that card.
    """
    # Splitting the line to get the part after the colon (:)
    _, numbers = card_line.split(':')

    # Splitting the numbers into winning numbers and own numbers
    winning_numbers, own_numbers = numbers.split('|')
    winning_numbers = set(map(int, winning_numbers.split()))
    own_numbers = map(int, own_numbers.split())

    # Calculating points
    points = 0
    for number in own_numbers:
        if number in winning_numbers:
            points = 1 if points == 0 else points * 2

    return points


def count_matching_numbers(winning_numbers, own_numbers):
    """
    Count the number of matching numbers between the winning and own numbers.
    """
    return sum(1 for number in own_numbers if number in winning_numbers)

def process_scratchcards(data):
    """ Process the scratchcards and return the total number of scratchcards."""

    # Initialize count array with 1 for each card (as each card exists initially)
    card_counts = [1] * len(data)

    for i, card_line in enumerate(data):
        _, numbers = card_line.split(':')
        winning_numbers, own_numbers = numbers.split('|')
        winning_numbers = set(map(int, winning_numbers.split()))
        own_numbers = map(int, own_numbers.split())

        matches = count_matching_numbers(winning_numbers, own_numbers)

        # Add the count to subsequent cards based on the number of matches and current count of the card
        for j in range(i + 1, min(i + 1 + matches, len(data))):
            card_counts[j] += card_counts[i]

    return card_counts


with open("input.txt") as file:
    lines = file.readlines()

    total_points = sum(parse_and_calculate_card_points(card) for card in lines)
    total_scratchcards = sum(process_scratchcards(lines))

    print("First puzzle solution:", total_points)
    print("Second puzzle solution:", total_scratchcards)

