#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 18 12/18/23
# Shawn Kroeger
#--------------------------------------------
import re
lagoon = []

def parse_data(file):
    ''' Returns the contents of the input file in a list '''
    with open(file, "r") as f:
        str_list = f.read().strip().split("\n")
        str_list = [list(i.split(" ")) for i in str_list]
    return str_list


def create_polygon(data, part2=False):
    ''' Put the vertices of a polygon into the lagoon list, and return the sum of the perimeter '''
    global lagoon
    x = y = 0
    sum_perimeter = 0
    lagoon.clear()
    
    for d in data:  # [Direction Qty Hex#]
        if (part2):
            h = re.search(r"\(#([0-9a-z]{5})([0-9a-z])\)", d[2])
            qty = int(h.group(1), 16)
            direction = h.group(2)
        else:
            qty = int(d[1])
            direction = d[0]
        
        match direction:
            case 'R' | '0': x += qty
            case 'D' | '1': y -= qty
            case 'L' | '2': x -= qty
            case 'U' | '3': y += qty
            case   _: raise NotImplementedError
        lagoon.append([x,y])        
        sum_perimeter += qty
    
    return sum_perimeter

        
def polygonArea(vertices):
    # Returns the area of a polygon using the Shoelace algorithm, given only vertices {#copied}
    # https://en.wikipedia.org/wiki/Shoelace_formula
    num_v = len(vertices) # Number of Vertices
    sum1 = sum2 = 0

    for i in range(0, num_v-1):
        sum1 = sum1 + vertices[i][0] *  vertices[i+1][1]
        sum2 = sum2 + vertices[i][1] *  vertices[i+1][0]

    sum1 = sum1 + vertices[num_v-1][0]*vertices[0][1]   #Add xn.y1
    sum2 = sum2 + vertices[0][0]*vertices[num_v-1][1]   #Add x1.yn
    area = abs(sum1 - sum2) / 2
    return area


if __name__ == "__main__":
    data = parse_data("Aoc18.txt")
    sum_perimeter = create_polygon(data)
    shoelace_area = polygonArea(lagoon)
    # From Pick's theorem using the Shoelace formula...
    # Shoelace returns area of a polygon, but we need to include perimeter area too.  This is the formula:
    total_area = shoelace_area + sum_perimeter/2 + 1
    print("Total area (including perimeter) =", int(total_area))
    # Part2:
    sum_perimeter = create_polygon(data, True)
    shoelace_area = polygonArea(lagoon)
    total_area = shoelace_area + sum_perimeter/2 + 1
    print("Total area (part 2) =", int(total_area))
    