#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 20 12/20/23 - Pulse Propagation
# Shawn Kroeger
#--------------------------------------------
import sys
from collections import deque

modules = {}   # 'name' -> Obj pointer: references the modules (class instances) described in the input file
Q = deque()    # Use a queue to keep pulses in the correct order
_rx_pulses = 0
_debug = 0

class Day20Obj:
    """ Base Class for Day 20 objects, defining common variables"""
    def __init__(self, name, conn_list):
        self.__name__ = name
        self.low_pulse_cnt = 0
        self.high_pulse_cnt = 0
        self.downstream = []  # downstream modules to send data to
        for i in conn_list:
            self.downstream.append(i)
    
    def list_downstream(self):
        return self.downstream
    
    def get_pulse_cnt(self):
        return self.low_pulse_cnt, self.high_pulse_cnt


class FlipFlop(Day20Obj):
    """ '%' Flip-Flop module: state = 'on' or 'off' (default).  Sends & receives pulses. """
    def __init__(self, name, conn_list):
        Day20Obj.__init__(self, name, conn_list)
        self.state = 'off'
    
    def send_pulse(self, sender, ptype):
        # Receiving: 'high' pulse: Ignore
        #            'low' pulse: flips the state between on and off  
        # Sending: on -> off: sends low pulse
        #          off -> on: sends high pulse
        if ptype == 'low':
            if self.state == 'off':
                self.state = 'on'
                for d in self.downstream:
                    self.high_pulse_cnt += 1
                    if _debug:
                        print("{} --> high to {}.  FF State = {}".format(self.__name__, d, self.state))
                    Q.appendleft([self.__name__, d, 'high'])
                    
            else:
                self.state = 'off'
                for d in self.downstream:
                    self.low_pulse_cnt += 1
                    if _debug:
                        print("{} --> low to {}.  FF State = {}".format(self.__name__, d, self.state))
                    Q.appendleft([self.__name__, d, 'low'])
                    


class Conjuntion(Day20Obj):
    """ '&' Conjunction module: remembers the type of the most recent pulse received from each
    upstream module.  Sends low pulse when all upstream modules last sent high, else sends high. """
    def __init__(self, name, conn_list):
        Day20Obj.__init__(self, name, conn_list)
        self.upstream = {}    # upstream modules with their last received pulse
    
    def add_sender(self, sender):
        if sender not in self.upstream:
            self.upstream[sender] = 'low'
        
    def send_pulse(self, sender, ptype):
        global _rx_pulses
        self.upstream[sender] = ptype
        for d in self.downstream:
            if 'low' in self.upstream.values():
                self.high_pulse_cnt += 1
                if _debug:
                    print("{} --> high to {}".format(self.__name__, d))
                if d in modules:
                    Q.appendleft([self.__name__, d, 'high'])
                elif d == 'rx':
                    _rx_pulses += 1
            else:
                self.low_pulse_cnt += 1
                if _debug:
                    print("{} --> low to {}".format(self.__name__, d))
                if d in modules:
                    Q.appendleft([self.__name__, d, 'low'])
                elif d == 'rx':
                    _rx_pulses += 1


class Broadcast(Day20Obj):
    """ Broadcasts received pulse to all downstream connected modules """
    def send_pulse(self, sender, ptype):
        for d in self.downstream:
            if ptype == 'low':
                self.low_pulse_cnt += 1
            else:
                self.high_pulse_cnt += 1
            if _debug:
                print("{} --> {} to {}".format(self.__name__, ptype, d))
            Q.appendleft([self.__name__, d, ptype])
            
            
def count_pulses(button_pushes):
    low_pulse_cnt = button_pushes # every button push sends a low pulse to the broadcaster
    high_pulse_cnt = 0
    
    for m in modules:
        lpc, hpc = modules[m].get_pulse_cnt()
        low_pulse_cnt += lpc
        high_pulse_cnt += hpc
    
    print("Low pulse count: {}, High pulse count: {}".format(low_pulse_cnt, high_pulse_cnt))
    print("Total # Pulses: {}".format(low_pulse_cnt*high_pulse_cnt))
    return low_pulse_cnt*high_pulse_cnt


def init_system():
    ''' Returns the contents of the input file in a list '''
    global modules
    with open(sys.argv[1], "r") as f:
        connections = f.read().strip().split("\n")

    conjunctions = []
    for i in connections:
        mod, *dest_list = i.split(" -> ")
        dest = dest_list[0].split(",")
        dest = [i.strip() for i in dest]
        if mod == "broadcaster":
            x = Broadcast("broadcaster", dest)
            modules["broadcaster"] = x
        elif mod[0] == '&':
            x = Conjuntion(mod[1:], dest)
            modules[mod[1:]] = x
            conjunctions.append(mod[1:])
        elif mod[0] == '%':
            x = FlipFlop(mod[1:], dest)
            modules[mod[1:]] = x
        else:
            raise ValueError
    
    # Initialize the conjunctions with their upstream senders
    for key in modules:
        for d in modules[key].list_downstream():
            if d in conjunctions:
                modules[d].add_sender(key)


def push_button(cnt, part2=False):
    """ Send "cnt" number of button pushes to the Broadcaster module using data connected modules """
    global _rx_pulses
    print("Pushing button (up to) {} time(s)".format(cnt))
    for i in range(cnt):
        _rx_pulses = 0
        if _debug:
            print("Button --> low to broadcaster")
        
        Q.appendleft(["button", "broadcaster", "low"])
        while Q:
            src, dest, ptype = Q.pop()
            modules[dest].send_pulse(src, ptype)
        
        if _rx_pulses == 1:
            print("Saw a single pulse sent to rx module! Button pushes = {}".format(i+1))
            break
        elif _debug:
            print("Button Presses={}, RX Pulses={}".format(i+1, _rx_pulses))


if __name__ == "__main__":
    _debug = 0
    N = 1000
    init_system()
    push_button(N)
    count_pulses(N)
