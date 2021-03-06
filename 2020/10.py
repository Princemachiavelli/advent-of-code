#!/usr/bin/env pypy3

import re
import sys
import time
from typing import List, Match, Optional
from copy import copy, deepcopy
from functools import lru_cache
test = False
debug = False
stdin = False
INFILENAME = "inputs/10.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/10.test.txt"
    if arg == "--debug":
        debug = True
    if arg == "--stdin":
        stdin = True


# Utilities
def rematch(pattern: str, s: str) -> Optional[Match]:
    return re.fullmatch(pattern, s)


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
    N = set([int(x) for x in lines])
    D = max(N)
    A = 3
    R = copy(N)
    diff = {}
    diff[3] = 1
    last = 0 
    while len(R) > 0:
        d = min(R)
        if d-last not in diff:
            diff[d-last] = 1
        else:
            diff[d-last] += 1
        last = d
        R.remove(d)
    print(diff)
    return diff[1] * diff[3]

#@lru_cache(maxsize=None)
cache = dict()

def numPaths(l: frozenset, t: int, maxDiff: int = 3):
    global cache
    if (l,t,maxDiff) in cache:
        return cache[(l,t,maxDiff)]
    if t <= maxDiff:
        cache[(l,t,maxDiff)] = 1
        return cache[(l,t,maxDiff)]
    if len(l) == 0:
        cache[(l,t,maxDiff)] = 0
        return cache[(l,t,maxDiff)]
    if sum(l) < t - maxDiff:
        cache[(l,t,maxDiff)] = 0
        return cache[(l,t,maxDiff)]
    if len(l) == 1:
        if (t - set(l).pop()) <= maxDiff:
            cache[(l,t,maxDiff)] = 1
            return cache[(l,t,maxDiff)]
        else:
            cache[(l,t,maxDiff)] = 0
            return cache[(l,t,maxDiff)]
    n = 0
    for c in l:
        nl = l - frozenset([c])
        n += numPaths(nl, t - c) + numPaths(nl, t)
    cache[(l,t,maxDiff)] = n
    return cache[(l,t,maxDiff)]

@lru_cache(maxsize=None)
def numPaths2(l: frozenset, c: int, t: int, maxDiff: int = 3):
    if c + maxDiff >= t:
        return 1 + len(l)
        #for a in l:
        #    if a < t:
        #        yield 1
    elif len(l) == 0:
        return 0
    else:
        nextAdapter = list(l)[0]
        rest = list(l)[1:]
        if c + maxDiff < nextAdapter: 
            return 0
        else:
            nl = frozenset(sorted(rest))
            return numPaths2(nl, nextAdapter, t, maxDiff) + numPaths2(nl, c, t, maxDiff)

# Dynamic Program -> go backwords
def part2() -> int:
    N = frozenset(sorted([int(x) for x in lines]))
    D = max(N) + 3
    print(f"D = {D}")
    #for i in range(min(N), D):
    #    numPaths2(N,0,10,3)
    return numPaths2(N, 0, D, 3)

print("Part 2")
print(part2())
