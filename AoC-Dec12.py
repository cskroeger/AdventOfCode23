#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 12 12/12/23
# Shawn Kroeger
#--------------------------------------------
import re
configs = {}

# Hot Springs
# Search Rules:
# A '#' is definitely in the match pattern and must be filled
# A '?' is a wildcard and can either match a '#' or '.'
# A '.' is not in the match pattern
# There must be at least one '.' between matches
# Find the total number of arrangements of each line, then sum each line's total
#
# Inputs: strg = input string on which to operate
#       groups = number of groups
# Output: number of possible ways to fit the input group onto the input record
# Sample Input:
# ?#????#??#.???#.##? 7,1,1,1,2
# ?#???#????????.?? 5,2,4,1
# ???????????# 3,1,1,3
def find_matches(strg, groups):
    global configs
    lst = ''.join([str(i) for i in groups])
    if (strg + lst) in configs:  # If this pattern has been seen, lookup and return the result
        return configs[strg + lst]
    
    num_possibilities = 0
    n = groups[0]        # Length of current group.  We must have this many ? or # in a row
    match = re.search(r"^[#?]{%d}" %(n), strg[:n])
    
    if match and not (len(strg) > n and strg[n] == '#'):    # Found a match! And next char isn't a #
        new_grp = groups[1::]   # Reduce groups by 1 and search for remaining solution
        if len(strg) > n+1 and new_grp != []:
            fm = find_matches(strg[n+1:], new_grp)
            configs[strg[n+1:] + ''.join([str(i) for i in new_grp])] = fm
            num_possibilities += fm
        elif (new_grp == [] and re.search(r"#", strg[n:]) == None):  # Ensure no #s were left behind
            num_possibilities += 1
    
    if len(strg) > 1 and strg[0] != '#':  # cannot bypass #s; they must be consumed
        fm = find_matches(strg[1:], groups)
        configs[strg[1:] + ''.join([str(i) for i in groups])] = fm
        num_possibilities += fm
    
    return num_possibilities


def parse_data(file, part2=False):
    ''' Advent of Code 2023: Day 12, Hot Springs.
    Parse input file and decode it line by line, adding the resulting possible arrangements and returning the sum of them. '''
    total_arrangements = 0
    with open(file, "r") as f:
        for line in f:
            record, nums = line.strip().split(" ")
            nums = list(nums.split(","))
            nums = [int(i) for i in nums]
            if part2:  # duplicate the record and numbers 5x/ea
                record += ("?" + record) * 4
                nums *= 5
            line_arrangements = find_matches(record, nums)
            print(record, nums, "=> Arrangements:", line_arrangements)
            if line_arrangements == 0:
                print("ERROR: no arrangements found.  Exiting.")
                quit()
            total_arrangements += line_arrangements
            configs.clear()
    return total_arrangements


if __name__ == "__main__":
    print("Total Arrangements (part 1) =", parse_data("Aoc12.txt"))
    print("Total Arrangements (part 2) =", parse_data("Aoc12.txt", True))
    