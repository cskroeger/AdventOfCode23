#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 1 12/1/23
# Shawn Kroeger
#--------------------------------------------
import re

def convert_num(din):
   '''convert written numbers into digits, but still an ASCII character.
   Pass numerical digits (and all other characters) through without changing them. '''
   match din:
      case "one":   out = "1"
      case "two":   out = "2"
      case "three": out = "3"
      case "four":  out = "4"
      case "five":  out = "5"
      case "six":   out = "6"
      case "seven": out = "7"
      case "eight": out = "8"
      case "nine":  out = "9"
      case "zero":  out = "0"
      case _:       out = din
   return out;


def calc_sum(file_in):
   ''' Sum of all the two-digit numbers extracted from each line of an input file, 
   where the first and last number of a character string are concatenated together 
   to form the two-digit number.  Numbers can be in the format "two" or "2". '''
   d1 = d2 = ''
   sum_out = 0
   pattern = "(one|two|three|four|five|six|seven|eight|nine|zero|\d)"
   
   with open(file_in, "r") as f:
      for line in f:
         match = re.search(pattern + "+?.*" + pattern, line)
         if match:
            d1 = convert_num(match.group(1))
            d2 = convert_num(match.group(2))
         
         else:  # the first regex doesn't find strings that only have a single number.  Fix that here
            try2 = re.search(pattern + "+?.*", line)
            d1 = d2 = convert_num(try2.group(1))
         
         sum_out += int(d1 + d2)
         #print (line, d1 + d2, " => SUM =", sum_out)  # debug
            
   f.close()
   return sum_out

if __name__ == "__main__":
   print ("sum =", calc_sum("Aoc1.txt"))
