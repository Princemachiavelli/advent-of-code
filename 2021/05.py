#!/usr/bin/env pypy3

import re
import sys
import time
from lolviz import *
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict
from itertools import repeat
from functools import partial
from advent import sirange, srange, nddict
import pprint
import math
if type(__builtins__) is not dict or 'profile' not in __builtins__: profile=lambda f:f;


ADVENTDAY="05"
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
print("Part 1:")

@profile
def part1() -> int:
    global pp
    G = defaultdict(int)
    for l in lines:
        s,e = l.split('->')
        x1,y1 = map(int,s.split(','))
        x2,y2 = map(int,e.split(','))
        xm = 1 if x2 >= x1 else -1
        ym = 1 if y2 >= y1 else -1
        if x1 == x2 or y1 == y2: 
            for x in sirange(x1, x2):
                for y in sirange(y1, y2):
                    G[(x,y)] += 1
    O = 0
    for v in [y for y in G.values() if y > 1]:
        O += 1
    return O

print(part1())

@profile
def part2():
    global ADVENTDAY, test, pp
    G = defaultdict(int)
    for l in lines:
        s,e = [map(int,x.split(',')) for x in l.split('->')]
        x1,y1 = s
        x2,y2 = e
        if test:
            pp(locals())
        if x1 == x2 or y1 == y2: 
            for x in sirange(x1, x2):
                for y in sirange(y1, y2):
                    G[(x,y)] += 1
        else:
            # Assumes 45 degree slope?
            # python 3.10 added a strict parameter to check
            for x,y in zip(sirange(x1,x2),sirange(y1,y2)):
                G[(x,y)] += 1
    return len([y for y in G.values() if y > 1])

print("Part 2:")
print(part2())






























