#!/usr/bin/env pypy3

import re
import sys
import time
import statistics
import numpy as np
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


ADVENTDAY="07"
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

def cost(x,y):
    return sum(range(1,abs(x-y)+1))

def l2(x: list, p: int = 2):
    return sum(abs(y)**p for y in x)**(1/p)

def pm(x: list):
    return 1/len(x)*sum(x)


# [1, 4, 9]
def part1() -> int:
    global ADVENTDAY, test, pp
    C = sorted([int(x) for x in lines[0].split(',')])
    #M = statistics.(C)
    G = defaultdict(int)
    for c in range(0,max(C)): 
        minCost = None
        minPos = C[0]
        for x in C:
            cc = cost(x,c)
            G[c] += cc
    mostMin = None
    least = min(G.values())
    for k,v in G.items():
        if v == least:
            mostMin = k
    T = 0
    for c in C:
        T += cost(c, mostMin)
    print(f"l2 = {l2(C,4)}")
    print(np.mean(C))
    print(sum(C)/len(C))
    print(f"mostMin = {mostMin}")
    return T

print(part1())

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
    return 0 


print("Part 2:")
#print(part2())
























