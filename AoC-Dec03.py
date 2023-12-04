#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 3 12/3/23
# Shawn Kroeger
#--------------------------------------------
import re

# Globals
LINE_LEN = 140
#LINE_LEN = 20   # Test case
sym1 = sym2 = sym3 = LINE_LEN * "."  # Create arrays of strings representing symbol locations ("S")

# Dictionary defined as: "Line#_Start#" : [start position, end position, value]
# examples:
#{'0_1': [1, 3, 242], '0_10': [10, 12, 276], '0_17': [17, 19, 234]}
#{'3_0': [0, 2, 344], '3_11': [11, 13, 340]}
sch1 = sch2 = sch3 = {}  # dict of 3 lines worth of #s.  We'll process the middle while looking above & below
running_sum = 0;         # sum of part numbers that are deemed legal
gear_ratio_sum = 0;


def line_to_dict(line, lnum):
    ''' Input a line from the schematic and put numbers into a dictionary '''
    line_dict = {}
    for m in re.finditer(r"\d+", line):  # look for numbers
        #print('%03d: %02d-%02d: %s' % (lnum, m.start(), m.end()-1, m.group(0)))
        key = str(lnum) + "_" + str(m.start(0))
        line_dict[key] = [m.start(), m.end()-1, int(m.group(0))]
    #print (line_dict)
    return line_dict

def get_min_line(n):
    if (n == 0): return 0
    else:        return (n-1)

def get_max_line(n):
    if (n == LINE_LEN-1): return n
    else:                 return (n+1)

def list_valid_idx(n):
    ''' Valid indices for adjacent gear ratios '''
    if (n == 0): 
        return [0, 1]
    elif (n == LINE_LEN-1):
        return [n-1, n]
    else:
        return [n-1, n, n+1]

def sum_eng_parts_sch2():
    ''' Process schematic line 2, checking lines above (1) and below (3) for symbols (S & G) adjacent
    to numbers.  When this occurs, return the sum of valid part numbers on the current line. '''
    sumlv = 0
    
    for key, value in sch2.items():
        hit = False;
        # If any of the following cases are true, add the number to the running total
        # check for symbol before the number
        if ((value[0] != 0) and ((sym2[value[0]-1] == 'S') or (sym2[value[0]-1] == 'G'))):
            hit = True
        # check for symbol after the number
        elif ((value[1] != (LINE_LEN-1)) and ((sym2[value[1]+1] == 'S') or (sym2[value[1]+1] == 'G'))):
            hit = True
        else:  # check for symbol above or below the number
            for n in range(get_min_line(value[0]), get_max_line(value[1])+1):
                if ((sym1[n] == 'S') or (sym1[n] == 'G')): hit = True   # check for symbol on previous line
                if ((sym3[n] == 'S') or (sym3[n] == 'G')): hit = True   # check for symbol on next line
                
        if (hit):
            sumlv = sumlv + value[2]

    return sumlv


def sum_gears_sch2():
    ''' Process schematic line 2, checking lines above (1) and below (3) for gears (G).  When present,
    if there are exactly 2 numbers adjacent to the gear, multiply the numbers together and return the
    sum of all such occurrences on the current line. '''
    sumg = 0

    for idx, g in enumerate(sym2):   # Check for "G" in the sym2 array, then check for exactly 2 surrounding #s
        if (g != "G"):
            continue
        gears = []
        range_of_valid_idx = list_valid_idx(idx)
        #print ("valid_idx=", range_of_valid_idx)
        
        # If any of the following cases are true, add the gear ratio to the running total
        for nums in sch2:
            if ((idx != 0) and sch2[nums][1] == idx-1):  # check for number before the G
                gears.append(sch2[nums][2])
            if ((idx != LINE_LEN-1) and sch2[nums][0] == idx+1):  # check for number after the G
                gears.append(sch2[nums][2])
        
        # check for numbers on previous line
        for nums in sch1:
            for i in range(sch1[nums][0], sch1[nums][1]+1):
                for valid_i in range_of_valid_idx:
                    if (i == valid_i):
                        gears.append(sch1[nums][2])
                        break
                else:
                    continue
                break
        
        # check for numbers on subsequent line
        for nums in sch3:
            for i in range(sch3[nums][0], sch3[nums][1]+1):
                for valid_i in range_of_valid_idx:
                    if (i == valid_i):
                        gears.append(sch3[nums][2])
                        break
                else:
                    continue
                break
        
        # Valid gear ratios will have exactly 2 numbers.  If so, multiply together and add to result
        if (len(gears) == 2):
            sumg = sumg + (gears[0]*gears[1])
        #print ("   Adjacent gear numbers:", gears)
    
    return sumg


def process_line(line, lnum):
    ''' update line dictionaries.  Newest goes into sch3, push the others down. Then process sch2. '''
    global sch1, sch2, sch3, sym1, sym2, sym3, running_sum, gear_ratio_sum   # ensure global scope of vars
    sch1 = sch2
    sym1 = sym2
    sch2 = sch3
    sym2 = sym3
    sch3 = line_to_dict(line, lnum)
    sym3 = re.sub(r"[\*]","G", line.strip())    # Put a 'G' wherever there is a gear
    sym3 = re.sub(r"[^\d.G]","S", sym3)         # Put an 'S' wherever there is a non-gear symbol
    #print ("\n", sym1, "\n", sym2, "\n", sym3)
    #print (sch2, "=>", sym2)
    running_sum = running_sum + sum_eng_parts_sch2()
    gear_ratio_sum = gear_ratio_sum + sum_gears_sch2()


def process_instr_manual(file_in):
    ''' Day 3, challenge 1.  Count engine parts.
    Engine parts are defined as numbers in the input file adjacent to any symbol, either on
    the same line or an adjacent line.  Diagonals count. 
        Challenge 2: sum gear ratios.
    Gear ratios are defined as "*" adjacent to exactly two numbers, either on the same line
    or an adjacent line, where diagonals count.'''
    lnum = 0;  # Line #
    with open(file_in, "r") as f:
        for line in f:
            process_line(line, lnum)
            lnum=lnum+1
        process_line(LINE_LEN * ".", lnum)   # one more call is needed since process_line counts the middle line
            
    f.close()
    print ("Sum of Engine Parts =", running_sum)
    print ("Sum of Gear Ratios =", gear_ratio_sum)


if __name__ == "__main__":
    #process_instr_manual("Aoc3_test.txt")
    process_instr_manual("Aoc3.txt")
