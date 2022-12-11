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


ADVENTDAY="08"
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

def visible(M, r, c, h, dirr, first=False):

    if (r,c) in M and M[(r,c)] >= h and not first:
        yield 0 
    elif r >= MAXR or c >= MAXC:
        yield 0
    elif r <= 0 or c <= 0:
        yield 0
    else:
        yield 1 
        if dirr == "R":
            yield from visible(M,r,c+1,h, dirr)
        elif dirr == "L":
            yield from visible(M,r,c-1,h, dirr)
        elif dirr == "U":
            yield from visible(M,r-1,c,h, dirr)
        elif dirr == "D":
            yield from visible(M,r+1,c,h, dirr)


def part1():
    global MAXC, MAXR
    V = 0
    M = defaultdict(int)
    MAXR = len(lines)-1
    MAXC = len(lines[0])-1
    for r,l in enumerate(lines):
        for c,h in enumerate(l):
            M[(r,c)] = int(h)
    MM = 0
    for l,h in M.items():
        zz = 1
        for z in "UDLR":
            t = sum(visible(M, l[0], l[1], h, z, True))
            zz *= t
        MM = max(MM,zz)

    print(f"ans = {MM}")

part1()


def part2():
    print()

#part2()
def check(M, r, c, h):
    RB = []
    RA = []
    CB = []
    CA = []
    for k,v in M.items():
        if k[0] == r:
            if k[1] > c:
                CB.append(v)
            if k[1] < c:
                CA.append(v)
        if k[1] == c:
            if k[0] > r:
                RB.append(v)
            if k[0] < r:
                RA.append(v)
    if r == 0 and c == 1:
        print(RB)
        print(RA)
        print(CB)
        print(CA)
    S = 1
    for i in RB:
        A = 0
        if i < h:
            A += 1
        S *= A
    for i in RA:
        A = 0
        if i < h:
            A += 1
        S *= A
    for i in CB:
        A = 0
        if i < h:
            A += 1
        S *= A
    for i in CA:
        A = 0
        if i < h:
            A += 1
        S *= A
    return S
    #return h > max(RB) or h > max(RA) or h > max(CB) or h > max(CA)
