#!/usr/bin/env pypy3

import re
import sys
import time
import statistics
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict
from itertools import repeat
from functools import partial
from advent import sirange, srange, nddict
import pprint
import math
from astar import * 
if type(__builtins__) is not dict or 'profile' not in __builtins__: profile=lambda f:f;
sys.setrecursionlimit(10000000)


ADVENTDAY="11"
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

C = 0
def flash(M, k):
    global C
    C += 1
    for r1,c1 in [(-1,-1),(-1,0),(0,-1),(+1,+1),(+1,0),(0,+1),(+1,-1),(-1,+1)]:
        rn = r1+k[0]
        cn = c1+k[1]
        if (rn,cn) in M.keys():
            M[(rn,cn)] += 1
            if M[(rn,cn)] == 10:
                M=flash(M, (rn,cn))
    return M

@profile
def part1() -> int:
    global ADVENTDAY, test, pp, C
    M = defaultdict(int)
    T = 0
    S = []
    for r, line in enumerate(lines):
        for c,l in enumerate(line):
            M[(r,c)] = int(l)
    print(M)

    for x in range(10000):
        C = 0
        print(f"Step {x+1}")
        for k,v in copy(M).items():
            M[k] += 1
        for k,v in copy(M).items():
            if v == 10:
                M = flash(M, k)
        for k,v in copy(M).items():
            if v > 9:
                M[k] = 0
        print(M.values())
        if len(M) == C:
            print("All flashed in {x+1}")
            return x+1
    return None 

print(part1())


#@profile
#def part2():
#    return 0 


print("Part 2:")
#print(part2())
























