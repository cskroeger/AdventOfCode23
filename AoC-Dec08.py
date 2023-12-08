#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 8 12/8/23
# Shawn Kroeger
#--------------------------------------------
import re
from math import lcm

instructions = []
mapp = {}

def parse_data(file, sep="\n"):
    ''' Formats input file into both a list of instructions, and a dictionary of paths to take (mapp). '''
    # Instructions are changed from [L=Left and R=Right] to [0,1] to make them useful for choosing the 
    # Left and Right indices of the mapp '''
    global instructions, mapp
    with open(file, "r") as f:
        str_list = f.read().strip().split(sep)
    
    inst = list(str_list[0])
    for i in inst:
        instructions.append(0 if (i == 'L') else 1)
    
    str_list.pop(0)
    str_list.pop(0)
    
    for s in str_list:
        mm = re.search("(\w+) = \((\w+), (\w+)\)", s)
        mapp[mm.group(1)] = [mm.group(2), mm.group(3)]


def solve_puzzle_p1(inp, part2=False):
    ''' Find path to done for an individual value '''
    idx = 0       # Current index of the instruction list.  Rolls over
    counter = 0   # Number of steps to reach solution
    max_idx = len(instructions)
    key = inp
    while not key.endswith('Z' if part2 else 'ZZZ'):
        key = mapp[key][instructions[idx]]
        counter += 1
        idx = 0 if (idx == max_idx-1) else idx+1
    return counter


def solve_puzzle_p2():
    ''' Start from all paths that end in 'A' simultaneously, then for each path search for its solution,
    where a soln ends in 'Z'.  This would take a really long time using a search methodology.  But since
    paths are cyclical, solve for each path and find the Least Common Multiple.'''
    start = [i for i in mapp.keys() if i.endswith('A')]
    print("  Part 2 starting positions:", start)
    steps = [solve_puzzle_p1(i, True) for i in start]
    print("  Steps required for each starting position:", steps)
    return lcm(*steps)
    

if __name__ == "__main__":
    parse_data("Aoc8.txt")
    print("** Number of steps required, part 1: %d" %(solve_puzzle_p1('AAA')))
    print("** Number of steps required, part 2: %d" %(solve_puzzle_p2()))