# Objetive: Create the environment to train. Try playing with 6 randomized bots.

import random
from enum import Enum

# Define the cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Create a deck
deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# Create bots
class Bot:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.seat = -1
        self.position = -1
        self.stack = 100
        self.bet = 0

    def receive_cards(self, cards):
        self.hand = cards
    
    def set_position(self, position):
        self.position = position

def deal_cards(deck, num_bots):
    hands = []
    for _ in range(num_bots):
        hand = [deck.pop(), deck.pop()]
        hands.append(hand)
    return hands


def save_hand_to_file(log, file_name):
    with open(file_name, 'a') as file:
        for entry in log:
            file.write(entry + '\n')
        file.write('-' * 40 + '\n')

def assign_poker_positions(button_seat, total_seats=6):
    """
    Assign positions to seats based on the given button seat for a 6-max poker table.
    
    :param button_seat: The seat where the button is located (number from 1 to 6).
    :param total_seats: The total number of seats (default is 6).
    :return: A dictionary where keys are seat numbers and values are their positions.
    """
    # Ensure the button_seat is within the valid range
    if button_seat < 1 or button_seat > total_seats:
        raise ValueError(f"button_seat must be between 1 and {total_seats}.")
    
    # Define the position mapping for a 6-max table
    positions_mapping = {
        0: 'Button',
        1: 'Cutoff',
        2: 'Middle Position',
        3: 'Early Position',
        4: 'Big Blind',
        5: 'Small Blind'
    }
    
    # Calculate the position for each seat based on the button_seat
    positions = {}
    for i in range(total_seats):
        seat = (button_seat - 1 + i) % total_seats
        positions[seat + 1] = positions_mapping[i]
    
    return positions

class PokerStreet(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3




######## Play Hand ########
def play_hand(bots, deck, log):

    shuffled_deck = shuffle_deck(deck.copy())
    
    # Deal cards
    log.append("Dealing cards.")
    hands = deal_cards(shuffled_deck, len(bots))
    
    for bot, hand in zip(bots, hands):
        bot.receive_cards(hand)
        log.append(f'{bot.name} received {hand}.')

    # Set positions
    button_seat = random.randint(1, 6)
    if bot.seat == button_seat:
            bot.position = 0
            log.append(f'{bot.name} Position {0}.')

    positions = assign_poker_positions(button_seat)

    for bot in bots:
        bot.position = positions[bot.seat]
        if bot.position == 4:
            bot.bet = 1
        if bot.position == 5:
            bot.bet = 0.5

        print(f"Position of {bot.name} in seat {bot.seat}: {bot.position}")

    
    street = 0
    max_bet = 1
    players_to_talk = 5
    showdown = False
    last_action_position = 4

    # 1. Hand is finished?
    while not showdown and players_to_talk > 0:

        # 2. Calculate next position
        next = next_position_to_talk(street, last_action_position)

        # 3. Calculate posible actions and choose an action
        

        # 4. Street is finished?



    # Simulate board cards
    board = [shuffled_deck.pop() for _ in range(5)]
    log.append(f'Board cards: {board}')

    # Determine winner (simplified, currently random)
    winner = random.choice(bots)
    log.append(f'The winner is {winner.name}.')

    return winner
#####################################


def main(num_hands, file_name):
    bots = [Bot(f'Bot {i}') for i in range(1, 7)]
    deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]

    i = 1
    for bot in bots:
        bot.seat = i
        bot.name = "Bot" + str(i)
        i += 1

    with open(file_name, 'w') as file:
        file.write('Poker Hand Log\n')
        file.write('=' * 40 + '\n')

    for _ in range(num_hands):
        log = []
        winner = play_hand(bots, deck, log)
        save_hand_to_file(log, file_name)

if __name__ == '__main__':
    num_hands = 1  # You can change the number of hands to simulate
    file_name = 'poker_log.txt'
    main(num_hands, file_name)
