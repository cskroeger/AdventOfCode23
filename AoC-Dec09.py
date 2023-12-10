#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 9 12/9/23, Mirage Maintenance
# Shawn Kroeger
#--------------------------------------------
import re

data = []

def parse_file(file, sep="\n"):
    ''' Returns the contents of the input file in a list, with entries separated by sep '''
    global data
    with open(file, "r") as f:
        data = f.read().strip().split(sep)
    for idx, i in enumerate(data):
        data[idx] = list(i.split(' '))
    for idx, i in enumerate(data):
        for idx2, j in enumerate(i):
            data[idx][idx2] = int(j)


def get_next_value(inp, part2=False):
    ''' Recursive function that will take a sequence of integers and find either:
    Part 1: the next value of the sequence, or
    Part 2: the previous vale of the sequence '''
    nxt = []  # next list, where where values are defined as msb-lsb of each pair of numbers
    for i in range(0, len(inp)-1):
        lsb, msb = inp[i:i+2]
        nxt.append(msb-lsb)
    #print(nxt)
    prev_last_val = 0
    recurse = False
    for i in nxt:
        if (i != 0):
            recurse = True
            break
    
    if (recurse):
        prev_last_val = get_next_value(nxt, part2)

    if part2:
        return inp[0] - prev_last_val 
    else:
        return inp[-1] + prev_last_val


def sum_next_values(part2=False):
    ''' Returns the sum of a list of "next values" of an input file, where next values
    are the next number in a sequence (or previous number, if part 2)'''
    next_vals = []
    for i in data:
        next_vals.append(get_next_value(i, part2))
    #print(next_vals)
    return sum(next_vals)


if __name__ == "__main__":
    parse_file("Aoc9.txt")
    print("Sum part 1 = %d" %(sum_next_values(False)))
    print("Sum part 2 = %d" %(sum_next_values(True)))
    
    