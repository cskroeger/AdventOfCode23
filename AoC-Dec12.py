#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 12 12/12/23
# Shawn Kroeger
#--------------------------------------------
import re

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
    num_possibilities = 0
    n = groups[0]        # Length of current group.  We must have this many ? or # in a row
    m = re.search(r"(^[#?]{%d})" %(n), strg[:n])  # Search for # or ? in the first n characters
    
    if m and (m.group(1) != None) and not (len(strg) > n and strg[n] == '#'):    # Found a match!
        new_grp = groups[1::]   # Reduce groups by 1 and search for remaining solution
        if len(strg) > n+1 and new_grp != []:
            num_possibilities += find_matches(strg[n+1:], new_grp)
        elif (new_grp == [] and re.search(r"#", strg[n:]) == None):  # Ensure no #s were left behind
            num_possibilities += 1
    
    if len(strg) > 1 and strg[0] != '#':  # cannot bypass #s; they must be consumed
        num_possibilities += find_matches(strg[1:], groups)
    
    return num_possibilities

# Part 2
# WARNING: The current implementation takes way too long; it's not yet viable
def unfold_records(record, nums):
    record += ("?" + record) * 4
    nums *= 5
    return record, nums


def parse_data(file, part2=False):
    ''' '''
    total_arrangements = 0
    with open(file, "r") as f:
        for line in f:
            record, nums = line.strip().split(" ")
            nums = list(nums.split(","))
            nums = [int(i) for i in nums]
            if part2:
                record, nums = unfold_records(record, nums)
            line_arrangements = find_matches(record, nums)
            total_arrangements += line_arrangements
            print(record, nums, "=> Arrangements:", line_arrangements)
    return total_arrangements
    print(record)


if __name__ == "__main__":
    print("Total Arrangements (part 1) =", parse_data("Aoc12_test.txt"))
    print("Total Arrangements (part 2) =", parse_data("Aoc12_test.txt", True))
    