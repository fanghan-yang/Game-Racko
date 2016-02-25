# Racko.py

import random

def shuffle(cardstack):
    '''shuffle the card stack'''
    random.shuffle(cardstack)

def check_racko(rack):
    '''check whether the rack is win'''
    for index in range(len(rack) - 1):
        if rack[index] < rack[index + 1]:   # each element should larger than the one after it
            return False
    return True

def get_top_card(card_stack):
    '''get the top card of the stack'''
    top_card = card_stack.pop()    # pop out the last element in the list, LIFO
    return top_card

def deal_initial_hands(deck):
    '''deal with the cards to initialize the game'''
    computer_hand = []
    user_hand = []
    for times in range(10):
        computer_hand.append(get_top_card(deck))
        user_hand.append(get_top_card(deck))
    return (computer_hand, user_hand)

def print_top_to_bottom(rack):
    '''print out a rack like a stack'''
    print
    print "Your rack is:"
    for index in range(len(rack)):
        print "             ", rack[index]
    print
        
def find_and_replace(new_card, card_to_be_replaced, hand, discard):
    if card_to_be_replaced in hand:
        add_card_to_discard(card_to_be_replaced, discard)
        hand[hand.index(card_to_be_replaced)] = new_card    # replace with new card
    else:
        print "    Oh, you don't have", card_to_be_replaced, "in your hand. Please try again."

def add_card_to_discard(card, discard):
    '''drop the card to the top of diacard pile'''
    discard.append(card)

def computer_check_completeness(hand):
    '''computer check the completeness of its cards, return a number representing the completeness of the hand'''
    completeness = 0        # initialize the completeness of the cards in hand
    for pos in range(9):
        if hand[pos] >= (9 - pos) * 6 - 2 and hand[pos] <= (9 - pos) * 6 + 9:
            completeness += 1       # if the card in the reasonable position, completeness + 1
            if hand[pos + 1] >= (8 - pos) * 6 - 2 and hand[pos + 1] < hand[pos]:
                completeness += 1   # if the next card is reasonable, completeness + 1
            else:
                completeness -= 1
        else:
            completeness -= 1
    if hand[9] > 9:
        completeness -= 1   # check the first card individually, since it is the last card in stack
    return completeness

def computer_strategy(hand, pile):
    '''computer's strategy regarding the completeness of its cards, return the position of a selected card'''
    completeness_init = computer_check_completeness(hand)   # get the initial completeness
    top = pile[-1]          # the top card of the pile
    completeness_list = []  # initialize a list to store all the completeness
    for pos in range(10):
        hand_temp = hand[:]
        hand_temp[pos] = top    # renew the hand and check its completeness
        completeness_list.append(computer_check_completeness(hand_temp))
    completeness_max = max(completeness_list)   # the maximum completeness in the list
    if completeness_max <= completeness_init:
        return None
    else:
        if completeness_list[9 - (top - 1) / 6] == completeness_max:
            return (9 - (top - 1) / 6)          # the most reasonable position has the priority
        else:
            return completeness_list.index(completeness_max)

def computer_play(hand, deck, discard_pile):
    '''computer's action'''
    pos = computer_strategy(hand, discard_pile)
    if pos is None:         # skip the top card of discard pile 
        pos = computer_strategy(hand, deck)
        deck_top = get_top_card(deck)
        if pos is None:     # skip the top card of deck
            add_card_to_discard(deck_top, discard_pile)
        else:               # keep the top card of deck
            add_card_to_discard(hand[pos], discard_pile)
            hand[pos] = deck_top
    else:                   # keep the top card of discard pile
        discard_top = get_top_card(discard_pile)
        add_card_to_discard(hand[pos], discard_pile)
        hand[pos] = discard_top
    return hand

def user_win(user_hand, computer_hand):
    '''user win'''
    print "**************************************************************"
    print "************************** Congrats **************************"
    print "**************************************************************"
    print "    Rack-O!"
    print "    You win!"
    print "    Your score:", (60 - user_hand[0] + user_hand[-1]) * 1000 + \
          sum([abs(element - 30) ** 2 for element in user_hand])
    print
    print "Computer's rack is:"
    for index in range(len(computer_hand)):
        print "             ", computer_hand[index]
    count = 0
    for index in range(len(computer_hand) - 1):
        if computer_hand[index] < computer_hand[index + 1]:
            count += 1
    if count <= 1:
        print "ENIAC: 'Almost there...'"
    else:
        print "ENIAC: 'I'll be more careful next time'"
    print
    print "Saving... Done!"
    print
    return

def computer_win(computer_hand):
    '''computer win'''
    print "**************************************************************"
    print "*************************** Defeat ***************************"
    print "**************************************************************"
    print "Computer's rack is:"
    for index in range(len(computer_hand)):
        print "             ", computer_hand[index]
    print "    Rack-O!"
    print "    Computer win!"
    print "    Computer score:", (60 - computer_hand[0] + computer_hand[-1]) * 1000 + \
          sum([abs(element - 30) ** 2 for element in computer_hand])
    print
    print "Saving... Done!"
    print
    return

def main():
    '''main process of the game'''
    deck = range(1, 61)
    discard = []
    shuffle(deck)
    hands = deal_initial_hands(deck)   # hands is a tuple
    computer_hand = hands[0]
    user_hand = hands[1]
    print_top_to_bottom (user_hand)
    discard.append(get_top_card(deck))     # reveal one card to begin the discard pile
    while True:
        print "************************* New Round *************************"
        discard_top = discard[-1]
        print "The top card in discard pile is:", discard_top
        firstChoice = 0
        while not(firstChoice == "y" or firstChoice == "n"):    # ask user input until it is acceptable
            firstChoice = raw_input("Do you want it (y/n)? ")
        print_top_to_bottom (user_hand)
        if firstChoice == "y":
            card_to_insert = get_top_card(discard)      # pop out the top card, rather than only check it
            while not(card_to_insert in user_hand):     # the top card of discard isn't in user's hand
                try:
                    card_to_be_replaced = input("Please select the card you want to kick out: ")
                except:
                    print "    Oh, card is number. Please try again."
                    continue
                find_and_replace(card_to_insert, card_to_be_replaced, user_hand, discard)
        else:
            deck_top = get_top_card(deck)
            print "The top card in deck is:", deck_top
            secondChoice = 0
            while not(secondChoice == "y" or secondChoice == "n"):  # ask user input until it is acceptable
                secondChoice = raw_input("Do you want it (y/n)? ")
            if secondChoice == "y":
                while not(deck_top in user_hand):     # the top card of discard isn't in user's hand
                    try:
                        card_to_be_replaced = input("Please select the card you want to kick out: ")
                    except:
                        print "    Oh, card is number. Please try again."
                        continue
                    find_and_replace(deck_top, card_to_be_replaced, user_hand, discard)
            else:
                discard.append(deck_top)
        print_top_to_bottom (user_hand)
        if check_racko(user_hand):
            user_win(user_hand, computer_hand)     # user win
            return
        if deck == []:
            deck = discard
            shuffle(deck)
            discard = []
            discard.append(get_top_card(deck))     # reveal one card to begin the discard pile
        computer_hand = computer_play(computer_hand, deck, discard) # computer's action
        if check_racko(computer_hand):
            computer_win(computer_hand)     # computer win
            return
        if deck == []:
            deck = discard
            shuffle(deck)
            discard = []
            discard.append(get_top_card(deck))     # reveal one card to begin the discard pile
        
if __name__ == '__main__':
    main()
