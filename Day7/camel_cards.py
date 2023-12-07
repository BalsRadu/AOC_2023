from collections import Counter
from functools import cmp_to_key

def rank_hand(hand, joker_rule=False):
    """
    Assigns a rank to a hand based on the Camel Cards rules, optionally including the joker rule.
    Returns the rank of the hand as an integer.
    """
    # Adjust the hand for the joker rule
    if joker_rule and 'J' in hand:
        counts = Counter(hand)
        counts['J'] = 0  # Remove 'J' from counts for finding the best replacement
        most_common_card, _ = counts.most_common(1)[0]
        hand = ''.join([most_common_card if card == 'J' else card for card in hand])

    counts = Counter(hand)
    count_values = counts.values()

    return (
        7 if len(counts) == 1 else
        6 if len(counts) == 2 and 4 in count_values else
        5 if len(counts) == 2 else
        4 if len(counts) == 3 and 3 in count_values else
        3 if len(counts) == 3 else
        2 if len(counts) == 4 else
        1
    )

def compare_hands(hand1, hand2, joker_rule=False):
    """
    Compares two hands based on their rank and the original order of card strengths.
    Returns -1 if hand1 is stronger, 1 if hand2 is stronger, and 0 if they are equal.
    """
    # Map the cards to their respective strengths, adjusting for joker rule if needed
    card_strength = {r: i for i, r in enumerate("23456789TJQKA", start=2)}
    if joker_rule:
        card_strength = {r: i for i, r in enumerate("J23456789TQKA", start=2)}

    rank1 = rank_hand(hand1[0], joker_rule)
    rank2 = rank_hand(hand2[0], joker_rule)

    # Compare based on rank
    if rank1 != rank2:
        return 1 if rank1 < rank2 else -1

    # Compare based on original order of card strengths
    for card1, card2 in zip(hand1[0], hand2[0]):
        if card1 != card2:
            return -1 if card_strength[card1] > card_strength[card2] else 1

    return 0  # Hands are equal


# Calculate total winnings without and with the joker rule
def calculate_total_winnings(hands, joker_rule=False):
    sorted_hands = sorted(hands, key=cmp_to_key(lambda x, y: compare_hands(x, y, joker_rule)), reverse=True)
    return sum(bid * (i+1) for i, (_, bid) in enumerate(sorted_hands))


# Open the input file and read the lines
with open("input.txt") as file:
    lines = file.readlines()

    # Parse the input and calculate the rankings
    hands = [(line.split()[0], int(line.split()[1])) for line in lines]

    # Print the solutions
    total_winnings1 = calculate_total_winnings(hands, joker_rule=False)
    total_winnings2 = calculate_total_winnings(hands, joker_rule=True)
    print("First puzzle solution:", total_winnings1)
    print("Second puzzle solution:", total_winnings2)



