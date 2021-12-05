#!/usr/bin/env pypy3

import re
import sys
import time
from typing import List, Match, Optional
from copy import copy, deepcopy
import math
test = False
debug = False
stdin = False
INFILENAME = "inputs/05.txt"
for arg in sys.argv:
    if arg == "--test":
        test = True
        INFILENAME = "inputs/05.test.txt"
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

covered = dict()
def part1() -> int:
    global covered
    #N = set([int(x) for x.split('->') in lines])
    for l in lines:
        s,e = l.split('->')
        x1,y1 = s.split(',')
        x2,y2 = e.split(',')
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        if x2 < x1:
            t = copy(x1)
            x1 = x2
            x2 = t
        if y2 < y1:
            t = copy(y1)
            y1 = y2
            y2 = t

        if x1 == x2 or y1 == y2: 
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    if x not in covered:
                        covered[x] = dict()
                    if y not in covered[x]:
                        covered[x][y] = 0
                    covered[x][y] += 1
                    print((x,y, covered[x][y]))
    O = 0
    for x in covered:
        for y in covered[x]:
            if covered[x][y] > 1:
                O += 1
    return O

#print(part1())


def part2():
    global covered
    covered = {}
    #N = set([int(x) for x.split('->') in lines])
    for l in lines:
        s,e = l.split('->')
        x1,y1 = map(int,s.split(','))
        x2,y2 = map(int,e.split(','))
        xm = 1 if x2 > x1 else -1
        ym = 1 if y2 > y1 else -1
        ym = 1
        if x2 < x1:
            xm = -1
        if y2 < y1:
            ym = -1

        if x1 == x2 or y1 == y2: 
            for x in range(x1, x2+1*xm, xm):
                for y in range(y1, y2+1*ym, ym):
                    if x not in covered:
                        covered[x] = dict()
                    if y not in covered[x]:
                        covered[x][y] = 0
                    covered[x][y] += 1
        elif abs((x2-x1)) == abs((y2-y1)):
            for i in range(0, abs(x2-x1)+1):
                x = x1+i*xm
                y = y1+i*ym
                print((i,x,y))
                if x not in covered:
                    covered[x] = dict()
                if y not in covered[x]:
                    covered[x][y] = 0
                covered[x][y] += 1
        elif x2 > x1 ^ y2 > y1 and False:
            break
            xm = 1
            ym = 1
            if x2 > x1:
                xm = -1
            if y2 > y1:
                ym = -1
            for i in range(0, abs(y2)-abs(y1)+1*ym):
                x = x1+i*xm
                y = y1+i*ym
                if x not in covered:
                    covered[x] = dict()
                if y not in covered[x]:
                    covered[x][y] = 0
                covered[x][y] += 1
    O = 0
    for x in covered:
        for y in covered[x]:
            if covered[x][y] > 1:
                O += 1
    return O

print(part2())






























