#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 5 12/5/23
# Shawn Kroeger
#--------------------------------------------
import re

# Globals: lists that get populated from input file
seeds = []
seed_to_soil = []
soil_to_fert = []
fert_to_water = []
water_to_light = []
light_to_temp = []
temp_to_humidity = []
humidity_to_loc = []
locations = []

def populate_seeds_list(inp):
    ''' copies input list (type: string) to global seeds list (type: int) '''
    global seeds
    inp.remove("seeds:")
    for i in inp:
        seeds.append(int(i))

        
def check_seed_validity(seed):
    ''' Returns True if input seed is part of the seed table, where the table
    is defined as pairs of (start, range) '''
    for i in range(0, len(seeds), 2):
        start, length = seeds[i:i+2]
        print("Checking seed %d validity in range %d-%d" %(seed, start, start+length-1))
        if ((seed >= start) and (seed < start+length)):
            return True  # Found a valid seed!
    return False


def find_match(db, inp, rev=False):
    ''' Find the destination corresponding to the source.  By default, the 
    data is interpreted as (DESTINATION, SOURCE, RANGE), but by setting the 
    rev flag, this can be changed to (SOURCE, DESTINATION, RANGE)'''
    if (rev):
        DST = 1
        SRC = 0
    else:
        DST = 0
        SRC = 1
    RNG = 2
    for ss in db:
        int_item = ss.split(" ")
        i_src = int(int_item[SRC])
        i_dest = int(int_item[DST])
        i_range = int(int_item[RNG])
                
        if ((inp >= i_src) and (inp <= i_src+i_range)):
            offset = inp - i_src
            #print("output=%d" %(i_dest + offset))
            return (i_dest + offset)
    #print("output=%d (default)" %(inp))
    return inp


def populate_list(inp, outp, match_str):
    ''' load the contents of the input "inp", i.e. data directly below the match_str,
    into the list "outp" '''
    load_list = False
    for idx, i in enumerate(inp):
        if (load_list):  # Data has been located; now load the output list
            if (i == ""):  # Exit condition: an empty list item
                #print(match_str, ":", outp)
                return
            outp.append(i)
        elif (re.match(match_str, i) != None):
            load_list = True   # found the match string; now start loading the list
    #print(match_str, ":", outp)  # End of file condition
    return


def find_loc(seed_in):
    ''' Returns a location associated with input seed '''
    my_soil     = find_match(seed_to_soil, seed_in)
    my_fert     = find_match(soil_to_fert, my_soil)
    my_water    = find_match(fert_to_water, my_fert)
    my_light    = find_match(water_to_light, my_water)
    my_temp     = find_match(light_to_temp, my_light)
    my_humidity = find_match(temp_to_humidity, my_temp)
    my_loc      = find_match(humidity_to_loc, my_humidity)
    #print("Seed=%s, Soil=%d, Fert=%d, Water=%d, Light=%d, Temp=%d, Humidity=%d => Loc=%d"
    #      % (seed, my_soil, my_fert, my_water, my_light, my_temp, my_humidity, my_loc))
    return my_loc

def find_seed(loc_in):
    ''' Returns a seed associated with input location '''
    my_humidity = find_match(humidity_to_loc, loc_in, True)
    my_temp     = find_match(temp_to_humidity, my_humidity, True)
    my_light    = find_match(light_to_temp, my_temp, True)
    my_water    = find_match(water_to_light, my_light, True)
    my_fert     = find_match(fert_to_water, my_water, True)
    my_soil     = find_match(soil_to_fert, my_fert, True)
    my_seed     = find_match(seed_to_soil, my_soil, True)
    print("Seed=%s, Soil=%d, Fert=%d, Water=%d, Light=%d, Temp=%d, Humidity=%d => Loc=%d"
          % (my_seed, my_soil, my_fert, my_water, my_light, my_temp, my_humidity, loc_in))
    return my_seed


def file_to_lists(file_in):
    ''' Parse the input file.  Put seeds and mappings into tables. '''
    global seeds
    flist = [line.rstrip() for line in open(file_in, "r")]
    populate_seeds_list(flist[0].split(" "))   # Put seeds into a list of ints
    #populate_seeds_list2(flist[0].split(" ")) # Part 2, Failed try #1
    populate_list(flist, seed_to_soil,     "seed-to-soil")
    populate_list(flist, soil_to_fert,     "soil-to-fertilizer")
    populate_list(flist, fert_to_water,    "fertilizer-to-water")
    populate_list(flist, water_to_light,   "water-to-light")
    populate_list(flist, light_to_temp,    "light-to-temperature")
    populate_list(flist, temp_to_humidity, "temperature-to-humidity")
    populate_list(flist, humidity_to_loc,  "humidity-to-location")
    

def find_closest_loc():
    ''' For each seed, find the corresponding location.  Then return the smallest
    number, i.e. closest location. '''
    global seeds, locations
    print("Seeds:", seeds)
    for seed in seeds:
        locations.append(find_loc(seed))
    
    closest_loc = min(locations)
    print("Closest Location (part 1) is %d" %(closest_loc))
    return closest_loc

def find_closest_loc_part2():
    ''' Work backwards: start with smallest location # and figure out if there is a valid
    seed for that location.  If not, increment location and try again.  Repeat until 
    a valid seed is found, which, by definition will be the closest seed. '''
    #global seeds, locations
    
    MIN_LOC = 56931765             # Min range (by looking at map data)
    #MAX_RANGE = 57000000    # Max range
    MAX_RANGE = 56931770    # Max range
    
    for loc in range(MIN_LOC, MAX_RANGE):
        seed = find_seed(loc)
        if (check_seed_validity(seed)):
            break
    if (loc == MAX_RANGE-1):
        print("Failed to find a valid seed within range %d - %d" %(MIN_LOC, MAX_RANGE))
    else:
        print("Closest Location (part 2) is %d, corresponding to seed %d" %(loc, seed))
    return loc
    
    
if __name__ == "__main__":
    #file_to_lists("Aoc5_test.txt")
    file_to_lists("Aoc5.txt")
    #find_closest_loc()
    find_closest_loc_part2()  # Output: 56931770 (after 2+ hours).  Wrong - too high