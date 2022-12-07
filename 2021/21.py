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
import pprint
import math
from astar import * 
if type(__builtins__) is not dict or 'profile' not in __builtins__: profile=lambda f:f;
sys.setrecursionlimit(10000000)


ADVENTDAY="21"
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

@profile
def part1():
    global lines, DICE, M
    P = defaultdict(int)
    S = defaultdict(int)
    S[5] = 20
    for i,l in enumerate(lines):
        o,s = l.split(':')
        P[i+1] = int(s.strip())

    R = 0
    K = True
    DICE = 1
    game(P[1], P[2], S[1], S[2], DICE)
    print(S)
    print(M)
    print(R)
    print('-'*30)
    return min(S[1],S[2]) * R 
print("Part 1:")
print(part1())
