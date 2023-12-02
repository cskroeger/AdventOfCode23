#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 2 12/2/23
# Shawn Kroeger
#--------------------------------------------
def dice_to_dictionary(dice):
    ''' Puts dice into a convenient dictionary for analysis
     Returns: dictionary out = {"blue": #, "red": #, "green": #}
     On Input: 'dice' string should look like the following: " 11 green, 4 red, 1 blue" 
     Only these 3 colors, all lowercase, in any order.  A color may be excluded. '''
    out = {"blue": 0, "red": 0, "green": 0}
    pairs = dice.split(",")
    for p in pairs:
        p = p.strip()  # input strings could have leading whitespace
        color = p.split(" ")
        out[color[1]] = int(color[0])
    return out


def find_max_dice(in1, in2):
    ''' Returns: dictionary with all 3 colors set to the maximum color associated with each input '''
    out = {"blue": 0, "red": 0, "green": 0}
    
    if in1["red"] > in2["red"]:      out["red"] = in1["red"]
    else:                            out["red"] = in2["red"]
    
    if in1["blue"] > in2["blue"]:    out["blue"] = in1["blue"]
    else:                            out["blue"] = in2["blue"]
    
    if in1["green"] > in2["green"]:  out["green"] = in1["green"]
    else:                            out["green"] = in2["green"]
    
    return out


def calc_power(dice):
    ''' Returns the values of the input dice dictionary multiplied together ''' 
    return dice["blue"] * dice["red"] * dice["green"]


def play_games(file_in):
    ''' Advent of Code Day 2 assignment has two goals:
    (1) Find the sum of all valid games played (valid = "doesn't exceed max predefined values per color")
    (2) calculate the sum of the power-of-sets of dice colors '''
    sum_valid_games = 0  # If a game can be played, add its game number to this var
    sum_power_sets = 0   # Accumulate the power of sets of dice that can be played
    
    with open(file_in, "r") as f:
        for line in f:
            valid_game = True  #staring assumption
            game_max = {"blue": 0, "red": 0, "green": 0}  # keep track of the max value of each color per game
            
            line = line.replace('\n', '')  #remove \n
            g = line.split(":", 1)         # Input string looks like "Game 30: blah blah"
            
            # Figure out the game number from "Game ##" string
            num = g[0].split(" ", 1)
            g_num = num[1]
            
            # Grab dice out of bag
            grab = g[1].split(";")  # Divide game into individual grabs of the dice
            for g in grab:
                roll = dice_to_dictionary(g)
                # Per the rules, if any color is > predefined max values, the game is not valid
                if ((roll["blue"]  > 14) or (roll["green"] > 13) or (roll["red"] > 12)):
                    valid_game = False
                    #break   -- we still want to check later grabs in order to update the game_max, so don't break
                game_max = find_max_dice(game_max, roll) # update game max for each roll
            
            #print (game_max)
            if valid_game:
                sum_valid_games += int(g_num)
            
            sum_power_sets = sum_power_sets + calc_power(game_max)
            
    f.close()
    print ("sum of valid games =", sum_valid_games)
    print ("sum of power of sets =", sum_power_sets)


if __name__ == "__main__":
    play_games("Aoc2.txt")
