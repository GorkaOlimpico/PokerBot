# Objetive: Create the environment to train. Try playing with 6 randomized bots.

import random
from enum import Enum

from ranking_hands import *

# Define the cards
suits = ['h', 'd', 'c', 's']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

# Create a deck
deck = [f'{rank}{suit}' for suit in suits for rank in ranks]

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
        self.in_hand = True

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
        if max_bet == 0 or max_bet == bot.bet:
            actions = ['check', 'bet']
            if bot.stack < max_bet:
                actions.pop()
        elif max_bet > bot.bet:
            actions = ['call', 'fold', 'bet']
            if max_bet >= bot.stack:
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
            bot.stack -= 1
        if bot.position == 5:
            bot.bet = 0.5
            bot.stack -= 0.5

        print(f"{bot.name} in " + position_in_table(bot.position)+ ": " + str(bot.hand[0]) +" "+ str(bot.hand[1]))

    print("----------")

    street = 0
    max_bet = 1
    players_in_hand = 6
    players_to_talk = 6
    showdown = False
    last_action_position = -1
    action_seat = -1
    players_allin = 0
    pot = 1.5

    # 1. Hand is finished?
    while not showdown and players_in_hand > 1 and players_to_talk > 0:

        # 2. Calculate next position
        next = next_position_to_talk(street, last_action_position, bots)

        for bot in bots:
            if bot.position == next:
                action_seat = bot.seat
                break

        # 3. Calculate posible actions and choose an action
        posible_actions = calculate_actions(max_bet, bots[action_seat])

        # Choose random action
        if posible_actions == []:
            print("Problema")

        if len(posible_actions) > 1:
            random_index = random.randint(0, len(posible_actions) - 1)
        else:
            random_index = 0

        if posible_actions[random_index] == 'bet':
            # Select bet amount with our stack
            if max_bet > 0:
                minimum_amount = max_bet*2
            else:
                minimum_amount = 1
            
            if bots[action_seat].stack < minimum_amount:
                bet_amount = bots[action_seat].stack
            else:
                bet_amount = round(random.uniform(minimum_amount, bots[action_seat].stack), 1)

            max_bet = round(bots[action_seat].bet + bet_amount, 1)

            
            
            bots[action_seat].bet += bet_amount
            bots[action_seat].stack = round(bots[action_seat].stack - bet_amount, 1)

            if bots[action_seat].stack == 0:
                players_allin += 1
                print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " bet Allin")

            players_to_talk = players_in_hand - 1
            pot += bet_amount
            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " bet:" + str(max_bet) + " | " + str(bots[action_seat].stack))

            
        elif posible_actions[random_index] == 'call':
            if max_bet >= bots[action_seat].stack + bots[action_seat].bet: # If call is Allin 
                bots[action_seat].bet = bots[action_seat].stack + bots[action_seat].bet
                call_amount = bots[action_seat].stack
                bots[action_seat].stack = 0
            else:
                if bots[action_seat].bet == 0:
                    call_amount = max_bet
                else:
                    call_amount = max_bet - bots[action_seat].bet
                
                bots[action_seat].stack = round(bots[action_seat].stack - call_amount, 1)
                bots[action_seat].bet = max_bet

            players_to_talk -= 1
            pot += call_amount

            if bots[action_seat].stack == 0:
                players_allin += 1
                print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " call Allin")

            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " call:" + str(round(call_amount,1)) + " | " + str(bots[action_seat].stack))
        
        elif posible_actions[random_index] == 'fold':
            bots[action_seat].hand = []
            players_in_hand -= 1
            players_to_talk -= 1
            bots[action_seat].in_hand = False
            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " fold")

            
        elif posible_actions[random_index] == 'check':
            players_to_talk -= 1
            print(f"{bots[action_seat].name} " + position_in_table(bot.position) + " check" + " | " + str(bots[action_seat].stack))


        last_action_position = bots[action_seat].position
        
        
        # 4. Street is finished or Allin?
        if players_allin > 0 and players_allin >= players_in_hand:
            print("Hand All-in")
            print("Pot: " + str(pot))
            while street <= 3:
                if street == 0:
                    print("All-in Preflop")
                    board = [shuffled_deck.pop() for _ in range(3)]
                    log.append(f'Board cards: {board}')
                elif street == 1:
                    print("All-in Flop")
                    board.append(shuffled_deck.pop())
                    log.append(f'Board cards: {board}')
                    print(f'Board cards: {board}')
                elif street == 2:
                    print("All-in Turn")
                    board.append(shuffled_deck.pop())
                    log.append(f'Board cards: {board}')
                    print(f'Board cards: {board}')
                elif street == 3:
                    print("All-in River")
                    print(f'Board cards: {board}')
                    showdown = True
                street += 1

        elif players_to_talk == 0 and players_in_hand > 1:
            if street < 3:
                street += 1
                if street == 1:
                    print("Flop")
                    board = [shuffled_deck.pop() for _ in range(3)]
                    log.append(f'Board cards: {board}')
                elif street == 2:
                    print("Turn")
                    board.append(shuffled_deck.pop())
                    log.append(f'Board cards: {board}')
                elif street == 3:
                    print("River")
                    board.append(shuffled_deck.pop())
                    log.append(f'Board cards: {board}')
                
                print(f'Board cards: {board}')
                print("Pot: " + str(round(pot)))


                players_to_talk = players_in_hand
                last_action_position = 0
                max_bet = 0
                for bot in bots:
                    bot.bet = 0

            else:
                showdown = True
        
        
    


    if showdown:
        # 1. Make a list with all of the hands of the players in hand
        hand_list = []
        for bot in bots:
            if bot.in_hand == True:
                hand_list.append(bot.hand)
                

        # 2. Parse all the hands
        #for hand in hand_list:
        #   hand[0], hand[1] = parse_poker_card(hand[0]), parse_poker_card(hand[1])

        # 3. Calculate best hand
        best_evaluations_list = []
        for hand in hand_list:
            best_evaluations_list.append(find_best_evaluation(hand, board))
            #print("Winners:", winners)
            #print("Best Hand:", best_hand)
            print("Best Evaluation:", best_evaluations_list[-1])

        # 4. Compare between best evaluations

    print("Hand finished")

    # Simulate board cards
    

    # Calculate winner
    #winner = calculate_winner(bots)
    #log.append(f'The winner is {winner.name}.')
    #print(f'The winner is {winner.name}.')

    return "winner"
#####################################


def main(num_hands, file_name):
    bots = [Bot(f'Bot {i}') for i in range(1, 7)]
    deck = [f'{rank}{suit}' for suit in suits for rank in ranks]

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
