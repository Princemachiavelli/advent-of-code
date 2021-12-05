#!/usr/bin/env pypy3

import re
import sys
import time
from typing import List, Match, Optional
from copy import copy, deepcopy

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


def part2() -> int:
def part1() -> int:
    N = set([int(x) for x in lines])
    D = max(N)

print(part1())
