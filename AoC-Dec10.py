#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 10 12/10/23 -- Pipe Maze
# Shawn Kroeger
#--------------------------------------------
import re

maze = [] # hold the contents of the input file in a list of lists
loop = [] # Store each loop value in list of lists

def parse_maze(file):
    ''' Returns the contents of the input file in a list'''
    global maze
    with open(file, "r") as f:
        maze = f.read().strip().split("\n")
    maze_width = len(maze[0])
    
    for i in range(0, len(maze)):
        loop.append([])


def move(curr_dir, y, x):
    ''' input the current direction being moved around the map, current x and current y coordinates '''
    # Top left corner of grid is 0,0
    turn = maze[y][x]
    #print(curr_dir, y, x, turn)
    if (curr_dir == 'E' and turn == '7'):
        nxt_dir, y, x = "S", y+1, x
    elif (curr_dir == 'E' and turn == '-'):
        nxt_dir, y, x = "E", y, x+1
    elif (curr_dir == 'E' and turn == 'J'):
        nxt_dir, y, x = "N", y-1, x

    elif (curr_dir == 'W' and turn == 'F'):
        nxt_dir, y, x = "S", y+1, x
    elif (curr_dir == 'W' and turn == '-'):
        nxt_dir, y, x = "W", y, x-1
    elif (curr_dir == 'W' and turn == 'L'):
        nxt_dir, y, x = "N", y-1, x

    elif (curr_dir == 'N' and turn == 'F'):
        nxt_dir, y, x = "E", y, x+1
    elif (curr_dir == 'N' and turn == '|'):
        nxt_dir, y, x = "N", y-1, x
    elif (curr_dir == 'N' and turn == '7'):
        nxt_dir, y, x = "W", y, x-1

    elif (curr_dir == 'S' and turn == 'L'):
        nxt_dir, y, x = "E", y, x+1
    elif (curr_dir == 'S' and turn == '|'):
        nxt_dir, y, x = "S", y+1, x
    elif (curr_dir == 'S' and turn == 'J'):
        nxt_dir, y, x = "W", y, x-1

    else:
        print("Error! Hit a roadblock.  Invalid maze:", curr_dir, y, x, turn)
        exit()
    return nxt_dir, y, x    


def first_dir(y, x):
    # Returns the new direction from any arbitrary starting point
    # Two out of four directions will be valid, so only need to check the first two
    if re.match("[-LF]", maze[y][x-1]):
        return 'W', y, x-1
    elif re.match("[|LJ]", maze[y-1][x]):
        return 'S', y+1, x
    else:
        return 'E', y, x+1


def sub_s(y, x):
    # An "S" will mess up part 2, so must be translated to its real variable
    global maze
    valids = []
    if re.match("[-LF]", maze[y][x-1]):
        valids.append('W')
    if re.match("[|LJ]", maze[y+1][x]):
        valids.append('S')
    if re.match("[-J7]", maze[y][x+1]):
        valids.append('E')
    if re.match("[|F7]", maze[y-1][x]):
        valids.append('N')
    match valids:
        case ["W", "S"]: s = "7"
        case ["W", "E"]: s = "-"
        case ["W", "N"]: s = "J"
        case ["S", "E"]: s = "F"
        case ["S", "N"]: s = "|"
    my_str = maze[y].replace("S", s)
    maze[y] = my_str
    print("** Replacing starting \"S\" with", s)
    

def find_farthest():
    ''' Trace maze around, find the length of the wall, then return (length / 2) for farthest wall brick'''
    global maze
    count = 0
    maze_width = len(maze[0])
    print("Maze Width:", maze_width)
    start_y = start_x = 0
    for start_y, s in enumerate(maze):
        for start_x in range(0, maze_width):
            if s[start_x] == 'S':
                break
        else:
            continue
        break
    print("Found start: [%d][%d], %s" %(start_y, start_x, maze[start_y][start_x]))
    curr_dir, y, x = first_dir(start_y, start_x)
    loop[y].append(x)
    count += 1
    while maze[y][x] != 'S':
        curr_dir, y, x = move(curr_dir, y, x)
        count += 1
        loop[y].append(x)
    sub_s(y, x)
    return count / 2


# Part 2
# A subset of the maze walls flip inside/outside.  Either "LJ" or "F7", plus walls "|"
# To see why, one needs a picture.
def calc_area():
    maze_width = len(maze[0])
    is_inside = False
    area = 0
    for y, line in enumerate(maze):
        line_area = 0
        loop[y].sort()
        for x in range(0, maze_width):
            if x in loop[y] and re.match("[|F7]", maze[y][x]):  # hit a maze wall
                is_inside = not is_inside
            elif x not in loop[y] and is_inside:
                line_area += 1
        #print(line, " Area enclosed: %d" %(line_area), loop[y])
        area += line_area
    return area
                

if __name__ == "__main__":
    parse_maze("Aoc10.txt")
    print("Farthest pipe is %d" %(find_farthest()))
    print("Area enclosed (take 2) by pipe maze is %d" %(calc_area()))
    
    