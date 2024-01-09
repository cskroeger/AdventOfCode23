#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 23 12/23/23 - A Long Walk
# Shawn Kroeger
#--------------------------------------------
import sys
from collections import deque

SQ = deque()  # use as a stack.  Values are lists of [y, x, dir, path_len, visited_list]
MAX_X = 0
MAX_Y = 0
PATH_LOOKUP = {}  # "Y_X_DIR" -> End_Y, END_X, End_Dir, Path length (only put stuff here if there are no intersections)
RECORDING = False
chain_key = ""
last_node = []  # y, x, dir of last_node, length of chain

def parse_data():
    global MAX_X, MAX_Y, PATH_LOOKUP
    with open(sys.argv[1], "r") as f:
        maze = f.read().strip().split("\n")
    idx = maze[0].find('.')
    SQ.append([0, idx, "S", 0, []])
    MAX_X = len(maze[0]) - 1
    MAX_Y = len(maze) - 1
    PATH_LOOKUP = {}
    return maze


# Part 2 explodes the state space, so here's the strategy to reduce it:
#  1) Only allow outside lanes to go 1 direction (S or E)
#  2) Record intersections visited.  Don't allow them to be visited a 2nd time (pushed onto stack)
#       Requires finding all intersections in the input map prior to start
#  3) Traverse lines between intersections only once.  Put them into a PATH_LOOKUP dictionary
def find_intersections(din):
    dout = []
    def is_intersection(y,x):
        nodes = 0
        if (y != 0 and din[y-1][x] != '#'):
            nodes += 1
        if (y != MAX_Y and din[y+1][x] != '#'):
            nodes += 1
        if (x != 0 and din[y][x-1] != '#'):
            nodes += 1
        if (x != MAX_X and din[y][x+1] != '#'):
            nodes += 1
        return nodes > 2
        
    for y in range(MAX_Y+1):
        line = ""
        for x in range(MAX_X+1):
            if (din[y][x] != '#' and is_intersection(y,x)):
                line += "i"
            else:
                line += din[y][x]
        dout.append(line)
    return dout


def record(y, x, dirc, symb, num_dirs):
    """ For Part 2, record paths between intersections so that they only need to be traversed once """
    global RECORDING, last_node, PATH_LOOKUP, chain_key
    if RECORDING:
        chain_len = last_node[3]
        if y == MAX_Y:
            last_node = [y, x, dirc, chain_len+1]
            PATH_LOOKUP[chain_key] = list(last_node)
            RECORDING = False
        elif symb == 'i':  # intersection
            if chain_len > 0:
                PATH_LOOKUP[chain_key] = list(last_node)
            else:  # If the path is 0-long, remove it
                del PATH_LOOKUP[chain_key]
            RECORDING = False
        elif num_dirs == 0:
            PATH_LOOKUP[chain_key] = [y, x, dirc, chain_len+1]  # A dead-end is dependent on prior intersections traversed
            RECORDING = False
        else:  # In a chain... update it
            last_node = [y, x, dirc, chain_len+1]
    elif num_dirs == 1 and not RECORDING:
        RECORDING = True
        chain_key = "{}_{}_{}".format(y,x,dirc)
        last_node = [y, x, dirc, 0]
        PATH_LOOKUP[chain_key] = []


def is_legal(dirc, symbol, y, x, visited):
    """ Determine if movement in this direction is allowed based on the direction and symbol encountered """
    if symbol == "#":
        return False
    # Limit perimeter directions to go E and S only
    elif ((y == 1 and dirc == "W") or (y == MAX_Y-1 and dirc == "W") or
          (x == 1 and dirc == "N") or (x == MAX_X-1 and dirc == "N")):
        return False
    elif symbol == ".":
        return True
    elif (PART2):
        return (y,x) not in visited
    else:
        match symbol:
            case ">": return dirc != "W"
            case "<": return dirc != "E"
            case "^": return dirc != "S"
            case "v": return dirc != "N"
            case _: raise ValueError("Unexpected data")
    
    
def get_legal_directions(dirc):
    """ Return a list of directions that are legal to take.  It is only illegal to go backwards """
    match dirc:
        case "N": return ["N", "E", "W"]
        case "S": return ["S", "E", "W"]
        case "E": return ["N", "S", "E"]
        case "W": return ["N", "S", "W"]
        case _: raise ValueError("Unexpected direction")


def get_new_coords(y,x,dirc):
    """ Input: last_node y,x coordinates and last_node direction
        Returns (True/False, new_y, new_x), where True means the new y,x coordinates are in-bounds """
    if ((dirc == "N" and y == 0) or (dirc == "S" and y == MAX_Y) or
       (dirc == "E" and x == MAX_X) or (dirc == "W" and x == 0)):
        return (False, y, x)
    match dirc:
        case "N": return (True, y-1, x)
        case "S": return (True, y+1, x)
        case "E": return (True, y, x+1)
        case "W": return (True, y, x-1)
        case _: raise ValueError("Unexpected direction")


def get_new_visited(y, x, symb, visited):
    """ Returns a new 'visited' list of coordinates where any intersection was seen on the last_node path """
    if PART2 and symb == 'i' and ((y,x) not in visited):
        visited.append((y,x))
    return visited

    
def traverse_maze(maze):
    max_path_len = 0
    
    while SQ:
        y, x, curr_dir, path_len, visited = SQ.pop()
        if DEBUG:
            print("Working on ({},{}):".format(y,x), curr_dir, path_len, visited)
        shortcut = "{}_{}_{}".format(y,x,curr_dir)
        
        if y == MAX_Y:
            max_path_len = max(path_len, max_path_len)
            record(y, x, curr_dir, maze[y][x], 0)
            if DEBUG:
                print(" $$ Finish line! Path length = {}".format(path_len))
        
        elif shortcut in PATH_LOOKUP:
            ny, nx, ndir, nlen = PATH_LOOKUP[shortcut]
            if DEBUG and (ny == MAX_Y or nlen > 0):
                print("    Shortcut: {}".format(shortcut), PATH_LOOKUP[shortcut])            
            if nlen > 0:
                SQ.append([ny, nx, ndir, nlen+path_len, list(visited)])
        
        else:
            num_dirs = 0
            new_visited = get_new_visited(y, x, maze[y][x], visited)
            for new_dir in get_legal_directions(curr_dir):
                coords_in_bounds, ny, nx = get_new_coords(y, x, new_dir)
                if coords_in_bounds and is_legal(new_dir, maze[ny][nx], ny, nx, visited):
                    num_dirs += 1
                    SQ.append([ny, nx, new_dir, path_len+1, list(new_visited)])
                    if DEBUG:
                        print("    Pushing:", ny, nx, new_dir, path_len+1)

            record(y, x, curr_dir, maze[y][x], num_dirs)
            if DEBUG:
                print("        Shortcuts:", PATH_LOOKUP)
    
    return max_path_len

                
if __name__ == "__main__":
    global PART2, DEBUG
    DEBUG = False
    PART2 = False
    print("Max path length (part 1) = {}".format(traverse_maze(parse_data())))
    PART2 = True
    print("Running part 2.  WARNING: this may take 5-10min...")
    print("Max path length (part 2) = {}".format(traverse_maze(find_intersections(parse_data()))))
