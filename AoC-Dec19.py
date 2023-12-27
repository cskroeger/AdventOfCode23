#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 19 12/19/23 - Aplenty
# Shawn Kroeger
#--------------------------------------------
import re
import operator
from collections import deque

MAXVAL = 4000
ops = {">":  operator.gt,
       "<":  operator.lt}
# workflows exs = {"in": [["s","<",1351,"px"],["qqz"]],
#                  "px": [["a","<",2006,"qkq"],["m",">",2090,"A"],["rfg"]]}
workflows = {}

def parse_data(file):
    """ Puts the contents of the input file into workflow and parts lists """
    global workflows
    wf = []
    pt = []
    
    with open(file, "r") as f:
        wf, pt = f.read().strip().split("\n\n")
        instructions, parts = wf.split("\n"), pt.split("\n")
    
    # Turn the input into workflows dictionary
    # input: in{s<1351:px,qqz}   or   px{a<2006:qkq,m>2090:A,rfg}
    for i in instructions:
        key, data = i.split("{")
        data2 = data.strip("}").split(",")
        # convert data2 from: 'a<2006:qkq','m>2090:A','rfg' ...to: ['a','<','2006','qkq'],['m','>','2090','A'],['rfg']
        val = []
        for d in data2:
            data3 = re.search(r"([xmas])([<>])([\d]+):(\w+)", d)
            if data3 != None:
                val.append([data3.group(1), data3.group(2), int(data3.group(3)), data3.group(4)])
            else:
                val.append([d])                     
        workflows[key] = val
    return parts


def sort_part(x,m,a,s,instr):
    """ Returns "A" for Accept or "R" for Reject for each input part based on a series of
    lookups through the global workflows instructions """
    lst = workflows[instr]
    
    for item in lst:  # An item looks like this: ["s","<",1351,"px"] or ["A"] or ["rfg"]
        if item[0] in {'A','R'}:
            return item[0]
        elif len(item) == 1:  # Recurse because we got another command to traverse
            return sort_part(x,m,a,s,item[0])
            
        typ, op, num, nextmap = item
        match typ:
            case "x": param = x
            case "m": param = m
            case "a": param = a
            case "s": param = s
            case _: raise ValueError
        if (ops[op](param,num)):
            break
    
    if nextmap in {'A','R'}:
        return nextmap
    else:
        return sort_part(x,m,a,s,nextmap)


def sum_passing_parts(parts):
    """ Takes a list of parts and sums the values of the passing parts """
    running_sum = 0
    for part in parts:
        inp = re.search(r"x=([\d]+),m=([\d]+),a=([\d]+),s=([\d]+)", part)
        x, m, a, s = int(inp.group(1)), int(inp.group(2)), int(inp.group(3)), int(inp.group(4))
        result = sort_part(x,m,a,s,"in")
        sumr = x + m + a + s if result == "A" else 0
        running_sum += sumr
        #print("Part {} -> {}, Sum = {}".format(part, result, sumr))
    return running_sum


def trace_paths(workflows, state):
    workflow_name, constraints = state
    for condition, target in workflows[workflow_name]['rules']:
        if condition is None:
            cons_true = constraints
        else:
            cons_true = add_constraint(constraints, condition)
            constraints = add_constraint(constraints, invert(condition))
        if cons_true is not None:
            if target == 'A':
                yield cons_true
            elif target != 'R':
                yield from trace_paths(workflows, (target, cons_true))


def get_min_max(op, n, lo, hi):
    match op:
        case '>':  lo = max(lo, n+1)
        case '<':  hi = min(hi, n-1)
        case '>=': lo = max(lo, n)
        case '<=': hi = min(hi, n)
        case _: raise ValueError
    return lo,hi


def get_ranges(var,op,n,xl,xh,ml,mh,al,ah,sl,sh):
    match var:
        case 'x': xl,xh = get_min_max(op, n, xl, xh)
        case 'm': ml,mh = get_min_max(op, n, ml, mh)
        case 'a': al,ah = get_min_max(op, n, al, ah)
        case 's': sl,sh = get_min_max(op, n, sl, sh)
        case _: raise ValueError
    return xl,xh,ml,mh,al,ah,sl,sh


# Credit to Jonathan Paulson for 'part2' algorithm.  After my solution didn't work
# out, I looked at several others and ended up 'leveraging' a variation of his:
# https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/19.py
def part2():
    running_sum = 0
    stack = deque([('in', 1, MAXVAL, 1, MAXVAL, 1, MAXVAL, 1, MAXVAL)])
    while stack:
        state,xl,xh,ml,mh,al,ah,sl,sh = stack.pop()
        #print(state,xl,xh,ml,mh,al,ah,sl,sh,running_sum)
        if state == 'R' or xl>xh or ml>mh or al>ah or sl>sh:
            continue
        elif state == 'A':
            running_sum += (xh-xl+1)*(mh-ml+1)*(ah-al+1)*(sh-sl+1)
            continue
        else:
            for cmd in workflows[state]:
                if len(cmd) > 1:
                    typ, op, num, nextmap = cmd
                    stack.append((nextmap, *get_ranges(typ,op,num,xl,xh,ml,mh,al,ah,sl,sh)))
                    xl,xh,ml,mh,al,ah,sl,sh = get_ranges(typ, '<=' if op=='>' else '>=', num,xl,xh,ml,mh,al,ah,sl,sh)
                else:
                    stack.append((cmd[0], xl, xh, ml, mh, al, ah, sl, sh))
                    break
    return running_sum


if __name__ == "__main__":
    parts = parse_data("Aoc19.txt")
    print("Part 1 Total: {}".format(sum_passing_parts(parts)))
    print("part 2 Total: {}".format(part2()))
