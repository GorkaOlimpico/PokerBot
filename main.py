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
    if button_seat < 0 or button_seat > total_seats:
        raise ValueError(f"button_seat must be between 1 and {total_seats}.")

    
    # Calculate the position for each seat based on the button_seat
    positions = {}
    for i in range(total_seats):
        seat = ((button_seat - 1 + i) % total_seats)
        positions[seat] = i
    
    return positions

class PokerStreet(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3

def calculate_actions(max_bet, bot):
    actions = []
    if bot.stack > 0:
        if max_bet == 0:
            actions = ['check', 'bet']
            if bot.stack < max_bet:
                actions.pop()
        elif max_bet > bot.bet:
            actions = ['call', 'fold', 'bet']
            if bot.stack < max_bet :
                actions.pop()
    
    
    return actions

def position_in_table(numero):
    posiciones = {
        4: "BB",
        5: "SB",
        0: "BTN",
        1: "CO",
        2: "MP",
        3: "EP"
    }
    return posiciones.get(numero, "Número no válido")
    

def next_position_to_talk(street, last_action_position, bots):
    position = last_action_position
    finded = False
    if street == 0 and last_action_position == -1:
        position = 3
    else:
        while not finded:
            if position == 0:
                position = 5
            else:
                position -= 1
            
            for bot in bots:
                if bot.position == position:
                    if bot.hand != [] and bot.stack > 0:
                        finded = True
                    break
            

    return position




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
    button_seat = random.randint(0, 5)
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

        print(f"Position of {bot.name} in seat {bot.seat}: " + position_in_table(bot.position))

    
    street = 0
    max_bet = 1
    players_in_hand = 6
    players_to_talk = 6
    showdown = False
    last_action_position = -1
    action_seat = -1
    players_allin = 0

    # 1. Hand is finished?
    while not showdown and players_in_hand > 1 and players_allin < players_in_hand - 1 :

        # 2. Calculate next position
        next = next_position_to_talk(street, last_action_position, bots)

        for bot in bots:
            if bot.position == next:
                action_seat = bot.seat
                break

        # 3. Calculate posible actions and choose an action
        posible_actions = calculate_actions(max_bet, bots[action_seat])

        # Choose random action
        if posible_actions ==  []:
            print("Problema")

        if len(posible_actions) > 1:
            random_index = random.randint(0, len(posible_actions) - 1)
        else:
            random_index = 0

        if posible_actions[random_index] == 'bet':
            # Select bet amount with our stack
            if max_bet+1 == bots[action_seat].stack:
                bet_amount = bots[action_seat].stack
                players_allin += 1
                print(f"{bots[action_seat].name} " + position_in_table(bot.position) + "Allin")
            else:
                bet_amount = random.randint(max_bet + 1, bots[action_seat].stack)

            bots[action_seat].bet = bet_amount
            max_bet = bet_amount
            bots[action_seat].stack = bots[action_seat].stack - bet_amount
            players_to_talk = players_in_hand - 1
            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " bet:" + str(bet_amount))

            
        elif posible_actions[random_index] == 'call':
            if max_bet > bots[action_seat].stack:
                bots[action_seat].bet = bots[action_seat].stack
                bots[action_seat].stack = 0
                players_allin += 1
            else:
                bots[action_seat].bet = max_bet
                bots[action_seat].stack = bots[action_seat].stack - max_bet
            players_to_talk -= 1
            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " call:" + str(max_bet))
        
        elif posible_actions[random_index] == 'fold':
            bots[action_seat].hand = []
            players_in_hand -= 1
            players_to_talk -= 1
            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " fold")

            
        elif posible_actions[random_index] == 'check':
            players_to_talk -= 1
            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " check")


        last_action_position = bots[action_seat].position
        

        # 4. Street is finished?
        if players_to_talk == 0 and players_in_hand > 1:
            if street < 3:
                street += 1
                if street == 1:
                    print("Flop")
                elif street == 2:
                    print("Turn")
                elif street == 3:
                    print("River")
                
                players_to_talk = players_in_hand
                last_action_position = 0
                max_bet = 0
                for bot in bots:
                    bot.bet = 0

            else:
                showdown = True

    print("Hand finished")

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

    i = 0
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
