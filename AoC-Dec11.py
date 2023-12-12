#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle ? 12/?/23
# Shawn Kroeger
#--------------------------------------------
import re

file = "Aoc11.txt"

# x,y (row, column) coordinates of all galaxies, numbered 1-n
# ex: {1:[0,4], 2:[1,9], 3:[2,0], 4:[5,8], 5:[6,1], 6:[7,12], 7:[10,9], 8:[11,0], 9:[11,5]}
galaxies = {}

def parse_data(file):
    global galaxies
    with open(file, "r") as f:
        gal_num = 1
        for idx, line in enumerate(f):
            line = line.strip()
            for i in range(0, len(line)):
                if (line[i] == "#"):
                    galaxies[gal_num] = [idx, i]
                    gal_num += 1

    
def expand_universe(file, part2=False):
    ''' For every empty column or row, add another adjacent to it '''
    global galaxies
    space = []
    with open(file, "r") as f:
        space = f.read().strip().split("\n")
    
    new_rows = []
    for idx, row in enumerate(space):
        if (re.search("#", row) == None):
            new_rows.append(idx)
    new_rows.reverse()
    #print("New Rows:\n", new_rows)
    
    new_columns = []
    for i in range(0, len(space[0])):
        for row in space:
            if (row[i] == "#"):
                break
        else:
            new_columns.append(i)
    new_columns.reverse()
    #print("New Columns:\n", new_columns)
    
    expander = 999999 if part2 else 1 
    for i in galaxies:
        for row in new_rows:
            if galaxies[i][0] > row:
                galaxies[i][0] += expander
        for column in new_columns:
            if galaxies[i][1] > column:
                galaxies[i][1] += expander
            

def calc_distances():
    total_distance = 0
    curr_distance = 0
    num_galaxies = len(galaxies)
    remaining_keys = list(galaxies.keys())
    remaining_keys.reverse()
    for k1 in galaxies:
        remaining_keys.pop()
        for k2 in remaining_keys:
            curr_distance = abs(galaxies[k1][0] - galaxies[k2][0]) + abs(galaxies[k1][1] - galaxies[k2][1])
            total_distance += curr_distance
            #print("Distance between stars %d & %d:" %(k1, k2), curr_distance, "  Running total:", total_distance)
    return total_distance

        
if __name__ == "__main__":
    parse_data(file)
    expand_universe(file, False) #Part 1
    #print(galaxies)
    print("Sum of Shortest Paths, Part 1 =", calc_distances())
    parse_data(file)
    expand_universe(file, True) #Part 2
    #print(galaxies)
    print("Sum of Shortest Paths, Part 2 =", calc_distances())
    