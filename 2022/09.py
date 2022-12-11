#!/usr/bin/env python3

import re
import sys
import time
import statistics
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict
from itertools import repeat
from functools import partial
#from advent import sirange, srange, nddict
import pprint
import math
#from astar import * 


ADVENTDAY="09"
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

def tailNextPos(h,t):
    print(f"head = {h}, tail = {t}")
    xd = h[0] - t[0]
    yd = h[1] - t[1]
    if abs(xd) <= 1 and abs(yd) <= 1:
        return t 
    if xd == 0 or yd == 0:
        if abs(xd) == 2:
            return (t[0] + xd/2, t[1])
        if abs(yd) == 2:
            return (t[0], t[1] + yd/2)
    else:
        #if abs(xd) + abs(yd) == 3:
        assert(abs(xd) + abs(yd) <= 4)
        return (t[0] + math.copysign(1, xd), t[1] + math.copysign(1, yd))
    return t

def next(h,l):
    d,n = l.split()
    n = int(n)
    if d == 'R':
        yield from [(h[0] + i + 1, h[1]) for i in range(n)]
    elif d == 'L':
        yield from [(h[0] - i - 1, h[1]) for i in range(n)]
    elif d == 'D':
        yield from [(h[0], h[1] - i - 1) for i in range(n)]
    elif d == 'U':
        yield from [(h[0], h[1] + i + 1) for i in range(n)]

def part1():
    V = set()
    h = (0,0)
    tails = [(0,0) for _ in range(10)]
    V.add(tails[-1])
    for l in lines:
        pp(tails)
        np = list(next(tails[0],l))
        for p in np:
            tails[0] = p
            print(tails)
            for i in range(0,len(tails)-1):
                print(i)
                print(tails)
                tails[i+1] = tailNextPos(tails[i], tails[i+1]) 
            V.add(tails[-1])
    A = len(V) 
    print(f"ans = {A}")

part1()


def part2():
    print()

#part2()
    #return h > max(RB) or h > max(RA) or h > max(CB) or h > max(CA)
