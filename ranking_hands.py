from itertools import combinations
from collections import Counter

# Definition of card values and suits
VALUES = "23456789TJQKA"
SUITS = "cdhs"
VALUE_DICT = {v: i for i, v in enumerate(VALUES, start=2)}

# Function to evaluate card value
def card_value(card):
    return VALUE_DICT[card[0]], card[1]

# Class to represent a poker hand
class PokerHand:
    def __init__(self, cards):
        self.cards = sorted(cards, key=card_value, reverse=True)
    
    def evaluate(self):
        if self.is_royal_flush() != None:
            is_straight_flush =  self.is_royal_flush()
        else:
            is_straight_flush =  " "
        
        if self.is_four_of_a_kind() != None:
            is_four_of_a_kind =  self.is_four_of_a_kind()
        else:
            is_four_of_a_kind =  " "
        
        if self.is_full_house() != None:
            is_full_house =  self.is_full_house()
        else:
            is_full_house =  " "

        if self.is_flush() != None:
            is_flush =  self.is_flush()
        else:
            is_flush =  " "

        if self.is_straight() != None:
            is_straight =  self.is_straight()
        else:
            is_straight =  " "
        
        if self.is_three_of_a_kind() != None:
            is_three_of_a_kind =  self.is_three_of_a_kind()
        else:
            is_three_of_a_kind =  " "

        if self.is_two_pair() != None:
            is_two_pair =  self.is_two_pair()
        else:
            is_two_pair =  " "
        
        if self.is_one_pair() != None:
            is_one_pair =  self.is_one_pair()
        else:
            is_one_pair =  " "
        
        if self.high_card() != None:
            high_card =  self.high_card()
        else:
            high_card =  " "

        return (
            is_straight_flush,
            is_four_of_a_kind,
            is_full_house,
            is_flush,
            is_straight,
            is_three_of_a_kind,
            is_two_pair,
            is_one_pair,
            high_card
        )

    def is_royal_flush(self):
        if self.is_straight_flush() and self.cards[0][0] == 'A':
            return (10,)
        return None
    
    def is_straight_flush(self):
        if self.is_flush() and self.is_straight():
            return self.high_card()
        return None
    
    def is_four_of_a_kind(self):
        counts = Counter(card[0] for card in self.cards)
        if 4 in counts.values():
            return max(counts, key=lambda x: (counts[x], VALUE_DICT[x]))
        return None
    
    def is_full_house(self):
        counts = Counter(card[0] for card in self.cards)
        if 3 in counts.values() and 2 in counts.values():
            return tuple(sorted((k for k, v in counts.items() if v >= 2), key=VALUE_DICT, reverse=True))
        return None
    
    def is_flush(self):
        counts = Counter(card[1] for card in self.cards)
        if 5 in counts.values():
            return tuple(sorted((card[0] for card in self.cards if card[1] == max(counts, key=counts.get)), key=VALUE_DICT, reverse=True))
        return None
    
    def is_straight(self):
        values = [card[0] for card in self.cards]
        value_indices = [VALUES.index(v) for v in values]
        value_indices = sorted(set(value_indices), reverse=True)
        if len(value_indices) < 5:
            return None
        for i in range(len(value_indices) - 4):
            if value_indices[i] - value_indices[i + 4] == 4:
                return VALUES[value_indices[i]]
        if 'A' in values and '2' in values and '3' in values and '4' in values and '5' in values:
            return '5'
        return None
    
    def is_three_of_a_kind(self):
        counts = Counter(card[0] for card in self.cards)
        if 3 in counts.values():
            return max(counts, key=lambda x: (counts[x], VALUE_DICT[x]))
        return None
    
    def is_two_pair(self):
        counts = Counter(card[0] for card in self.cards)
        pairs = [k for k, v in counts.items() if v == 2]
        if len(pairs) >= 2:
            return tuple(sorted(pairs, key=VALUE_DICT, reverse=True)[:2])
        return None
    
    def is_one_pair(self):
        counts = Counter(card[0] for card in self.cards)
        if 2 in counts.values():
            return max(counts, key=lambda x: (counts[x], VALUE_DICT[x]))
        return None
    
    def high_card(self):
        return tuple(card[0] for card in self.cards[:5])

# Function to find the best hand
def find_best_evaluation(hand, board):
    best_evaluation = None
    all_cards = hand + board
    for combo in combinations(all_cards, 5):
        poker_hand = PokerHand(combo)
        evaluation = poker_hand.evaluate()
        if best_evaluation == None:
            best_evaluation = evaluation
        elif evaluation > best_evaluation:
            best_evaluation = evaluation
    
    return best_evaluation

def parse_poker_card(card):
    # Check that the input string is exactly 2 characters long
    if len(card) != 2:
        raise ValueError("Invalid poker hand string. It should be exactly 2 characters long.")

    # Extract the value and the suit from the string
    value = card[0]
    suit = card[1]

    # Validate the value and the suit
    if value not in "23456789TJQKA" or suit not in "cdhs":
        raise ValueError("Invalid poker hand string. Value or suit is not valid.")

    # Return the tuple
    return (value, suit)


def format_poker_hand(card):
    # Check that the input is a tuple with exactly 2 elements
    if not isinstance(card, tuple) or len(card) != 2:
        raise ValueError("Invalid poker hand tuple. It should be a tuple with exactly 2 elements.")

    # Extract the value and the suit from the tuple
    value, suit = card

    # Validate the value and the suit
    if value not in "23456789TJQKA" or suit not in "cdhs":
        raise ValueError("Invalid poker hand tuple. Value or suit is not valid.")

    # Return the formatted string
    return f"{value}{suit}"








