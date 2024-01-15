#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 21 12/21/23 - Step Counter
# Shawn Kroeger
#--------------------------------------------
import sys
from collections import deque
from datetime import datetime

SQ = deque()  # use as a stack.  Values are lists of (y, x, 0/1), where the last # represents even/odd
MAX_X = 0
MAX_Y = 0
nodes = {}
next_nodes = set()
garden = []


def parse_data():
    global MAX_X, MAX_Y, garden
    with open(sys.argv[1], "r") as f:
        garden = f.read().strip().split("\n")
    MAX_X = len(garden[0]) - 1
    MAX_Y = len(garden) - 1
    for y in range(MAX_Y):
        for x in range(MAX_X):
            if garden[y][x] == 'S':
                start_y = y
                start_x = x
                break
        else:
            continue
        break
    SQ.append((start_y, start_x, 0))
    nodes["{}_{}".format(start_y, start_x)] = 0


def find_adjacents(y, x, eo):
    """ Puts (y,x,eo) into next_nodes ("eo" means even/odd).  Avoids previously traversed nodes. """
    global nodes, next_nodes, garden
    if (y != 0 and garden[y-1][x] != '#' and "{}_{}".format(y-1,x) not in nodes):
        next_nodes.add((y-1,x,eo))
    if (y != MAX_Y and garden[y+1][x] != '#' and "{}_{}".format(y+1,x) not in nodes):
        next_nodes.add((y+1,x,eo))
    if (x != 0 and garden[y][x-1] != '#' and "{}_{}".format(y,x-1) not in nodes):
        next_nodes.add((y,x-1,eo))
    if (x != MAX_X and garden[y][x+1] != '#' and "{}_{}".format(y,x+1) not in nodes):
        next_nodes.add((y,x+1,eo))
    
    
def traverse_garden(steps):
    global nodes, next_nodes, garden
    
    for i in range(steps+1):
        eo = (i+1)%2   # eo = 1 for odd numbers, 0 for even numbers
        {SQ.append(s) for s in next_nodes} # push all next_nodes endpoints onto stack
        next_nodes.clear()
        # Take a step.  Breadth-first search.  I.e., pop each position off of stack and move outward, taking 
        #   care not to repeat a previous point.  Put results in a local set called next_nodes
        while SQ:
            (y,x,eol) = SQ.pop()
            nodes["{}_{}".format(y,x)] = eol
            find_adjacents(y,x,eo)
    
    # Count possible endpoints, which is all nodes traversed that are either even or odd (whichever one 'steps' is)
    total = 0
    eo = steps%2
    for i in nodes:
        if nodes[i] == eo:
            total += 1
    return total
        

def print_time():
    now = datetime.now()
    current_time = now.strftime("%T.%f")[:-3]
    print(" --> Current Time =", current_time)
                
if __name__ == "__main__":
    global PART2, DEBUG
    DEBUG = False
    PART2 = False
    print_time()
    print("Running part 1...")
    parse_data()
    print("Number of garden nodes reached: {}".format(traverse_garden(64)))
    print_time()
