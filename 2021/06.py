#!/usr/bin/env pypy3

import re
import sys
import time
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict
from itertools import repeat
from functools import partial
from advent import sirange, srange, nddict
import pprint
import math
if type(__builtins__) is not dict or 'profile' not in __builtins__: profile=lambda f:f;
sys.setrecursionlimit(10000000)


ADVENTDAY="06"
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

NN = 2**16
print(f"NN = {NN}")
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

def part1() -> int:
    global ADVENTDAY, test, pp
    #G = defaultdict(int)
    G = []
    D = 6
    N = 1
    for f in [int(x) for x in lines[0].split(',')]:
        G.append(f)
    first = len(G)
    prev = len(G)
    S = []
    dd = 80
    if test:
        dd = 80 
    else:
        dd = 256
    for d in range(0, dd, 2):
        print(f"day {d}")
        new = []
        for i,v in enumerate(G):
            if v <= 0:
                G[i] = 6 + abs(v)
                new.append(8+abs(v))
            else:
                G[i] -= 2
        G += new
    return len(G)

#print(part1())

D = defaultdict(int)

@profile
def c(f: int, d: int):
    global D
    if (f,d) in D:
        return D[(f,d)]
    if f > d or d == 0:
        D[(f,d)] = 1
        return 1
    if f == 0:
        D[(f,d)] = c(0, d - 7) + c(0, d - 9)
        return D[(f,d)]
    else:
        n = min(f,d)
        s = c(f-n,d-n)
        D[(f-n,d-n)] = s
        return s

@profile
def part2():
    global ADVENTDAY, test, pp, NN, D
    N = dict()
    GG = []
    for f in [int(x) for x in lines[0].split(',')]:
        GG.append(f)
    for f in range(6, 0, -1):
        N[f] = c(f, NN)
    T = 0
    for f in GG:
        T += N[f]
    print(len(D))
    rate = defaultdict(int)
    return T 

def part22():
    global NN, D
    GG = defaultdict(int)
    for f in [int(x) for x in lines[0].split(',')]:
        GG[f] += 1
    for i in range(1,7):
        GG[0] += 1

print("Part 2:")
print(math.log(part2(),2))
























