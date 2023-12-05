#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 4 12/4/23
# Shawn Kroeger
#--------------------------------------------
import re

card_matches = {}  # {Card# : matches)
num_cards = []     # each index represents the number of copies of that card

def count_matches(line):
    ''' Count matches in the input string, where lines look like this:
    Card   1: 99 46 62 92 60 37 | 83 40 31 33 99  3 10 39 62 
    This is part 1.''' 
    sumv = 0
    s = re.search(r"([\d]+):([ \d]+) \| ([ \d]+)", line)
    winning_nums = s.group(2).split()
    match_nums   = s.group(3).split()
    for w in winning_nums:
        for m in match_nums:
            if (w==m):
                sumv = sumv+1
                break
    card_matches[s.group(1)] = sumv
    return sumv

def calc_points(n):
    if (n !=0):
        return 2**(n-1)
    else:
        return 0

def count_cards():
    ''' count cards according to the confusing rules of the game, part 2. 
    Copies of scratchcards are scored like normal scratchcards and have the same card number 
    as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, 
    it would then win a copy of the same cards that the original card 10 won: 
    cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you 
    to win any more cards. (Cards will never make you copy a card past the end of the table.)'''
    global card_matches, num_cards
    
    for k in card_matches.keys():
        num_cards.append(1)  # initialize an array of cards, 1 instance each
    
    #print("card_matches:", card_matches)
    for key, val in card_matches.items():
        cur_cnt = int(key)-1  # start with the current card number represented by the key
        cardn = cur_cnt
        for v in range(val):  # val represents the number of cards to increase
            cardn = cardn + 1
            num_cards[cardn] = num_cards[cardn] + num_cards[cur_cnt]
            #print("Adding cards (%s):" %(key), num_cards)
    
    return (sum(num_cards))
    

def calc_card_vals(file_in):
    global num_cards
    total_points = 0
    with open(file_in, "r") as f:
        for line in f:
            
            total_points = total_points + calc_points(count_matches(line))
    f.close()
    print ("total_points =", total_points)
    print ("total cards =", count_cards())
    print (num_cards)


if __name__ == "__main__":
    calc_card_vals("Aoc4.txt")
