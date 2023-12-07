#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 7 12/7/23
# Shawn Kroeger
#--------------------------------------------
# Sorted dictionary of hands, from worst hand to best
hands = {"high_card" : [], "one_pair": [], "two_pair": [], "three_kind": [],
         "full_house": [], "four_kind" : [], "five_kind" : []}

def reset_hands():
    global hands
    for i in hands:
        hands[i] = []


def xlate(x, wildcard=False):
    ''' orig  = [ A, K, Q, J, T,9,8,7,6,5,4,3,2,J*] => chars
        xlate = [14,13,12,11,10,9,8,7,6,5,4,3,2,1]  => ints
        wildcard: *optionally treat Jacks as wildcards; convert to value 1 '''
    if (wildcard and x == 'J'):
        return 1
    match x:
        case 'A': out = 14
        case 'K': out = 13
        case 'Q': out = 12
        case 'J': out = 11
        case 'T': out = 10
        case   _: out = int(x)
    return out


def file_hand(hand, bid, unique_cards, max_occurrence):
    global hands
    if (unique_cards == 5):
        hands["high_card"].append([hand, bid])
    elif (unique_cards == 4):
        hands["one_pair"].append([hand, bid])
    elif (unique_cards == 3 and max_occurrence == 2):
        hands["two_pair"].append([hand, bid])
    elif (unique_cards == 3 and max_occurrence == 3):
        hands["three_kind"].append([hand, bid])
    elif (unique_cards == 2 and max_occurrence == 3):
        hands["full_house"].append([hand, bid])
    elif (max_occurrence == 4):
        hands["four_kind"].append([hand, bid])
    elif (max_occurrence == 5):
        hands["five_kind"].append([hand, bid])  # What the....?  5 of the same cards?
    else:
        print("ERROR: This hand had no poker match.  Something went wrong.", hand)


def categorize_hand(hand, bid):
    ''' Categorize a 5-card hand into Poker hand types, optionally using Jacks (1) as wildcards.
    Output goes into hands dictionary '''
    cards = {i:hand.count(i) for i in hand}
    wildcards = 0
    if cards.get(1) != None:
        wildcards = cards[1]
        del cards[1]
    
    if wildcards == 5:  # 5 Wildcards?!?  good hand!
        cards[14] = 5
    elif wildcards > 0:
        high_val = high_key = 0
        for key in cards: # get the keys != 1
            # for the highest occurrence card, or card with highest value if occurrences are equal
            if ((cards[key] > high_val) or (cards[key] == high_val and key > high_key)):
                high_val, high_key = cards[key], key
        cards[high_key] = cards[high_key] + wildcards  # add wildcards to most numerous bucket
    
    unique_cards = len(cards)  # Number of unique cards
    max_occurrence = cards[max(cards, key=lambda key: cards[key])]  # Max times a card occurs
    file_hand(hand, bid, unique_cards, max_occurrence)
    #print(cards, "Wildcards: %d, unique=%d, max_occurrence=%d" %(wildcards, unique_cards, max_occurrence))

    
def calc_winnings():
    rank = 1
    out = 0
    for cat in hands:
        for bid in hands[cat]:
            out = out + (rank * bid[1])
            rank = rank + 1
    return out

            
def play_poker(file, part2=False):
    ''' Camel Poker, that is '''
    global hands
    with open(file, "r") as f:
        for line in f:
            hd = list(line.strip().split(" "))
            hd = [xlate(j, part2) for j in hd[0]], int(hd[1])
            categorize_hand(hd[0], hd[1])
    for key in hands:
        hands[key].sort()
    return calc_winnings()

                  
if __name__ == "__main__":
    part1 = play_poker("Aoc7.txt")
    print("Winnings part 1: %d" %(part1))
    #print(hands)
    reset_hands()
    part2 = play_poker("Aoc7.txt", True)
    print("Winnings part 2: %d" %(part2))
    #print(hands)
    