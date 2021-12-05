#!/usr/bin/env pypy3

import re
import sys
import time
from typing import List, Match, Optional

test = False
debug = False
stdin = False
INFILENAME = "inputs/09.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/09.test.txt"
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
    n = [int(x) for x in lines]
    for x in range(25, len(n)):
        n1 = n[x]
        h = False
        for p1 in n[x-25:x]:
            for p2 in n[x-25:x]:
                if p1 == p2:
                    continue
                if p1 + p2 == n1:
                    h = True
                    break
        if not h:
            return n1

print(part1())
s = "466456641"

c = dict()
def addRange(x, l, n):
    if (x,l) in c:
        return c[(x,l)]
    if l > 2:
        s = addRange(x, l - 1, n) + n[x + l]
        c[(x,l)] = s 
        return s
    else:
        s = sum(n[x:x+l])
        c[(x,l)] = s
        return s 

def part2() -> int:
    target = 466456641
    n = [int(x) for x in lines]
    for l in range(2, len(n)):
        for x in range(0, len(n) - l):
            #if addRange(x, l, n) == target:
            if sum(n[x:x+l]) == target:
                print((x,l))
                return min(n[x:x+l]) + max(n[x:x+l])
print(part2())
