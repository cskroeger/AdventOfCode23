#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 6 12/6/23
# Shawn Kroeger
#--------------------------------------------
import re

def boat_race(file_in, part):
    ''' Day 6: Calculating total ways to win a boat race. 
    Input Times are the total amount of time a race is in progress (in ms).
    Input Distances are the record distances of previous races (in mm).
    Holding button down for 1 ms makes the boat move 1mm/ms.  Holding the 
    button down for 2ms makes the boat move 2mm/ms.  Etc. '''
    f = [line.rstrip() for line in open(file_in, "r")]
    time = re.split("\s+", f[0])
    time.remove('Time:')
    distance = re.split("\s+", f[1])
    distance.remove('Distance:')
    
    newtime = ""
    newdist = ""
    if (part == 2):
        for i in time:
            newtime = newtime + i
        for j in distance:
            newdist = newdist + j    
    else:
        newtime = time
        newdist = distance
    print ("Time =", newtime)
    print ("Distance =", newdist)
    
    total_ways_to_win = 1
    for idx, race in enumerate(time):
        curr_ways_to_win = 0
        race_time = int(race)
        
        for speed in range(0, race_time):
            r_dist = speed*(race_time-speed)
            #print("Speed: %d, Distance: %d" %(speed, r_dist))
            if (r_dist > int(distance[idx])):
                curr_ways_to_win = curr_ways_to_win + 1
        total_ways_to_win = total_ways_to_win * curr_ways_to_win    
    
    print("Part %d: Total ways to win = %d\n" %(part, total_ways_to_win))


if __name__ == "__main__":
    boat_race("Aoc6.txt", 1)
    boat_race("Aoc6.txt", 2)