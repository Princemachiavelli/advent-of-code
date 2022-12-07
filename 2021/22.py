#!/usr/bin/env pypy3

import re
import json
import sys
import time
import heapq as hq
import statistics
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict, Counter
from itertools import repeat
from functools import partial
from advent import sirange, srange, nddict
from dataclasses import dataclass
import pprint
import math
from astar import * 
if type(__builtins__) is not dict or 'profile' not in __builtins__: profile=lambda f:f;
sys.setrecursionlimit(10000000)


ADVENTDAY="22"
test = False
debug = False
stdin = False
INFILENAME = f"inputs/{ADVENTDAY}.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = f"inputs/{ADVENTDAY}.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True

# Utilities
def rematch(pattern: str, s: str) -> Optional[Match]:
    return re.fullmatch(pattern, s)

def sirange(start: int, stop: int):
    stop += 1 if stop >= start else -1
    m = 1 if stop >= start else -1
    return range(start, stop, m)

def srange(start: int, stop: int):
    m = 1 if stop >= start else -1
    return range(start, stop, m)

def pp(stuff):
    print('-'*30)
    p = pprint.PrettyPrinter(indent=4, width=40, depth=3, compact=True)
    p.pprint(stuff)
    print('-'*30)

print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines()]

input_end = time.time()

# Part 1
########################################################################################

DICE = 1

M = defaultdict(int)
def roll(dice):
    s = dice 
    dice += 1
    dice = (dice - 1) % 100 + 1
    #M[s] += 1
    return (s, dice)

def turn1(pos, dice):
    #print(f"DICE = {DICE}")
    s = [None]*3
    s[0],dice = roll(dice)
    s[1],dice = roll(dice)
    s[2],dice = roll(dice)
    print(f"roll = {s}")
    pos += sum(s)
    pos = (pos - 1) % 10 + 1
    #print(f"pos: {oldPos} + {sum(s)%10}-> {pos}")
    return (pos, dice)

G = defaultdict(int)
def game(p1,p2,s1,s2,dice):
    while True: 
        #for k,v in copy(P).items():
        for p,s in [(p1,s1),(p2,s2)]:
            print(f"Player {p}")
            v = p
            newV, dice = turn1(v, dice)
            #print(f"newV = {newV}")
            p = newV
            s += newV
            if max([s1,s2]) >= 1000:
                return (s1,s2)

@dataclass
class cube:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int
    state: bool = True

    def contains(self, x: int, y: int, z: int) -> bool:
        if self.x1 <= x and x <= self.x2:
            if self.y1 <= y and y <= self.y2:
                if self.z1 <= z and z <= self.z2:
                    return True
        return False

    @classmethod
    def fromString(cls, line: str):
        reg = r'(?P<state>on|off)\sx=(?P<x1>\d+)\.+(?P<x2>\d+),y=(?P<y1>\d+)\.+(?P<y2>\d+),z=(?P<z1>\d+)\.+(?P<z2>\d+)'
        z = re.search(reg, line)
        if z is not None:
            m = z.groupdict()
            if m['state'] == 'on':
                state = True
            elif m['state'] == 'off':
                state = False

            return cls(int(m['x1']),int(m['x2']), int(m['y1']), int(m['y2']), int(m['z1']), int(m['z2']), state)
        else:
            print(f"Could not parse line: {line}")

@profile
def part1():
    global lines, DICE, M
    P = defaultdict(int)
    S = defaultdict(int)
    S[5] = 20
    for i,l in enumerate(lines):
        o,s = l.split(':')
        P[i+1] = int(s.strip())


print("Part 1:")
print(part1())
