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


ADVENTDAY="13"
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

def path(M, start='start', S = defaultdict(int)):
    for l in M[start]:
        pp(f"l = {l}")
        if l == 'start':
            continue
        if l == 'end':
            yield [start, l]
        elif l not in S or max(S.values()) < 2:
            if l.islower() or l == 'start' or l ==  'end':
                P  = copy(S)
                P[l] += 1
                for p in path(M, l, P):
                    yield [start] + p
            else:
                for p in path(M, l, S):
                    yield [start] + p
        else:
            print(f"Invalid Path {l}")
    print("Error")


def foldx(M, A):
    N = defaultdict(int)
    for x,y in M.keys():
        if x > A:
            nx = A - (x - A)
            print(f"{x} -> {nx}: {A}")
            N[(nx, y)] += M[(x,y)]
            #N[(nx, y)] += 1 
        if x < A:
            N[(x,y)] = max(N[(x,y)],M[(x,y)])
    return N

def foldy(M, A: int):
    N = defaultdict(int)
    for x,y in M.keys():
        if y > A:
            # 10 - (20 - 10) => 0
            # 10 - (15 - 10) => 5
            ny = A - (y - A)
            #print(f"{y} -> {ny}")
            #print(f"{x},{ny}")
            p = M[(x,y)]
            N[(x, ny)] += p
            if p > 1:
                print(f"mag: {p} -> {N[(x,ny)]}")

            #N[(x, ny)] += 1 
        if y < A:
            N[(x,y)] = max(N[(x,y)],M[(x,y)])
    return N


def g(M):
    global ADVENTDAY, test, pp, C, maxX, maxY
    for y in range(0,maxY+1):
        s = ''
        for x in range(0,maxX+1):
            if M[(x,y)] > 0:
                s += '#' + ''
            else:
                s += '.'
        print(s)
    print('-' * 25)

@profile
def part1() -> int:
    global ADVENTDAY, test, pp, C, maxX, maxY
    M = defaultdict(int)
    A = []
    maxX = 0
    maxY = 0
    for l in lines:
        if l == "":
            break
        x,y = l.split(',')
        x = int(x)
        y = int(y)
        if x > maxX:
            maxX = x
        if y > maxY:
            maxY = y
        M[(x,y)] = 1
    I = [l.split('=') for l in lines if 'fold' in l]
    pp(M)
    pp(I)
    if test:
        g(M)
    for k,v in I:
        print(k)
        if 'y' in k:
            M = foldy(M, int(v))
        if 'x' in k:
            M = foldx(M, int(v))
        if test:
            g(M)

    maxX = 0
    maxY = 0
    for x,y in M.keys():
        if x > maxX:
            maxX = x
        if y > maxY:
            maxY = y
    g(M)
    return len([x for x in M.values() if x > 0])

print(part1())


#@profile
#def part2():
#    return 0 


print("Part 2:")
#print(part2())
























