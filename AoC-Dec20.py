#!/usr/bin/env python3
#--------------------------------------------
# Advent of Code 2023
# Puzzle 20 12/20/23 - Pulse Propagation
# Shawn Kroeger
#--------------------------------------------
import sys
from collections import deque
from math import lcm

_modules_ = {} # 'name' -> Obj pointer: references the modules (class instances) described in the input file
Q = deque()    # Use a queue to keep pulses in the correct order
_rx_pulses_ = 0
_debug_ = 0

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
                    if _debug_:
                        print("{} --> high to {}.  FF State = {}".format(self.__name__, d, self.state))
                    Q.appendleft([self.__name__, d, 'high'])
                    
            else:
                self.state = 'off'
                for d in self.downstream:
                    self.low_pulse_cnt += 1
                    if _debug_:
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
        global _rx_pulses_
        self.upstream[sender] = ptype
        for d in self.downstream:
            if d == 'rx' and 'high' in self.upstream.values():  # there will only be 1 high at a time
                _rx_pulses_ += 1
            
            if 'low' in self.upstream.values():
                self.high_pulse_cnt += 1
                if _debug_:
                    print("{} --> high to {}".format(self.__name__, d))
                if d in _modules_:
                    Q.appendleft([self.__name__, d, 'high'])
            else:
                self.low_pulse_cnt += 1
                if _debug_:
                    print("{} --> low to {}".format(self.__name__, d))
                if d in _modules_:
                    Q.appendleft([self.__name__, d, 'low'])
    

class Broadcast(Day20Obj):
    """ Broadcasts received pulse to all downstream connected modules """
    def send_pulse(self, sender, ptype):
        for d in self.downstream:
            if ptype == 'low':
                self.low_pulse_cnt += 1
            else:
                self.high_pulse_cnt += 1
            if _debug_:
                print("{} --> {} to {}".format(self.__name__, ptype, d))
            Q.appendleft([self.__name__, d, ptype])
            
            
def count_pulses(button_pushes):
    low_pulse_cnt = button_pushes # every button push sends a low pulse to the broadcaster
    high_pulse_cnt = 0
    
    for m in _modules_:
        lpc, hpc = _modules_[m].get_pulse_cnt()
        low_pulse_cnt += lpc
        high_pulse_cnt += hpc
    
    print("P1 Button Pushes: {}, Low pulse count: {}, High pulse count: {}".format
             (button_pushes, low_pulse_cnt, high_pulse_cnt))
    print("P1: Total # Pulses: {}".format(low_pulse_cnt*high_pulse_cnt))
    return low_pulse_cnt*high_pulse_cnt


def init_system():
    global _modules_
    with open(sys.argv[1], "r") as f:
        connections = f.read().strip().split("\n")

    conjunctions = []
    for i in connections:
        mod, *dest_list = i.split(" -> ")
        dest = dest_list[0].split(",")
        dest = [i.strip() for i in dest]
        if mod == "broadcaster":
            _modules_["broadcaster"] = Broadcast("broadcaster", dest)
        elif mod[0] == '&':
            _modules_[mod[1:]] = Conjuntion(mod[1:], dest)
            conjunctions.append(mod[1:])
        elif mod[0] == '%':
            _modules_[mod[1:]] = FlipFlop(mod[1:], dest)
        else:
            raise ValueError
    
    # Initialize the conjunctions with their upstream senders
    for key in _modules_:
        for d in _modules_[key].list_downstream():
            if d in conjunctions:
                _modules_[d].add_sender(key)


def push_button(cnt):
    """ Send "cnt" number of button pushes to the Broadcaster module """
    print("Pushing button (up to) {} time(s)".format(cnt))
    last_rx_pulse = _rx_pulses_
    rx_feeders = []
    
    for i in range(cnt):
        if _debug_:
            print("Button --> low to broadcaster")
        
        Q.appendleft(["button", "broadcaster", "low"])
        while Q:
            src, dest, ptype = Q.pop()
            _modules_[dest].send_pulse(src, ptype)
        
        if i == 1000:
            count_pulses(i)
        
        if _rx_pulses_ != last_rx_pulse:
            rx_feeders.append(i+1)
            last_rx_pulse = _rx_pulses_
            if _debug_:
                print("Saw a pulse sent to rx module! Button pushes = {}".format(i+1))
            # For Part 2, there are four upstream modules from the module sending to rx.
            # When all of them have last sent a low, the module will also send a low.  Find the
            # least common multiple of the 4 sending blocks in lieu of waiting for it to happen.
            if len(rx_feeders) == 4:
                ans = 1
                for i in rx_feeders:
                    ans = lcm(ans, i)
                print("P2: {} button presses is the fewest to get a single low pulse to rx".format(ans))
                break


if __name__ == "__main__":
    _debug_ = 0
    N = 100000
    init_system()
    push_button(N)
    
