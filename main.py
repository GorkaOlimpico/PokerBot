# Objetive: Create the environment to train. Try playing with 6 randomized bots.

import random

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
        self.bet = 0

    def receive_cards(self, cards):
        self.hand = cards

    def make_bet(self):
        self.bet = random.randint(1, 100)

def deal_cards(deck, num_bots):
    hands = []
    for _ in range(num_bots):
        hand = [deck.pop(), deck.pop()]
        hands.append(hand)
    return hands

def play_hand(bots, deck, log):
    # Shuffle and log the action
    log.append("Shuffling the deck.")
    shuffled_deck = shuffle_deck(deck.copy())
    
    # Deal cards and log the action
    log.append("Dealing cards.")
    hands = deal_cards(shuffled_deck, len(bots))

    for bot, hand in zip(bots, hands):
        bot.receive_cards(hand)
        log.append(f'{bot.name} received {hand}.')
        bot.make_bet()
        log.append(f'{bot.name} bets {bot.bet}.')

    # Simulate board cards
    board = [shuffled_deck.pop() for _ in range(5)]
    log.append(f'Board cards: {board}')

    # Determine winner (simplified, currently random)
    winner = random.choice(bots)
    log.append(f'The winner is {winner.name}.')

    return winner

def save_hand_to_file(log, file_name):
    with open(file_name, 'a') as file:
        for entry in log:
            file.write(entry + '\n')
        file.write('-' * 40 + '\n')

def main(num_hands, file_name):
    bots = [Bot(f'Bot {i}') for i in range(1, 7)]
    deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]

    with open(file_name, 'w') as file:
        file.write('Poker Hand Log\n')
        file.write('=' * 40 + '\n')

    for _ in range(num_hands):
        log = []
        winner = play_hand(bots, deck, log)
        save_hand_to_file(log, file_name)

if __name__ == '__main__':
    num_hands = 10  # You can change the number of hands to simulate
    file_name = 'poker_log.txt'
    main(num_hands, file_name)
