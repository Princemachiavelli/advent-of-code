#!/usr/bin/env pypy3

import re
import sys
import time
import statistics
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict, Counter
from itertools import repeat
from functools import partial
from advent import sirange, srange, nddict
import pprint
import math
from astar import * 
if type(__builtins__) is not dict or 'profile' not in __builtins__: profile=lambda f:f;
sys.setrecursionlimit(10000000)


ADVENTDAY="14"
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

G = defaultdict(str)
@profile
def calc(T: str, R):
    global G
    OT = copy(T)
    if T in G:
        return G[T]
    if len(T) == 2:
        if T in R:
            G[T] = T[0] + R[T] + T[1]
    if len(T) > 2 and len(T) % 2 == 0:
        h = int(len(T)/2)
        #T = calc(T[0:h], R)[:-1] + calc(T[h-1:h+1], R) + calc(T[h:], R)[1:]
        G[T[0:h]] = calc(T[0:h], R)
        G[T[h-1:h+1]] = calc(T[h-1:h+1], R)
        G[T[h:]] = calc(T[h:], R)
        G[OT] = G[T[0:h]][:-1] + G[T[h-1:h+1]] + G[T[h:]][1:]
        return G[OT]
    if len(T) > 3 and len(T) % 2 == 1:
        h = int(len(T)/2)
        #T = calc(T[0:h], R)[:-1] + calc(T[h-1:h+1], R) + calc(T[h:], R)[1:]
        G[T[0:h]] = calc(T[0:h], R)
        G[T[h-1:h+1]] = calc(T[h-1:h+1], R)
        G[T[h:]] = calc(T[h:], R)
        G[OT] = G[T[0:h]][:-1] + G[T[h-1:h+1]] + G[T[h:]][1:]
        return G[OT]

    I = defaultdict(str)
    for i in range(0,len(T)-1):
        p = T[i:i+2]
        if p in R.keys():
            I[i+1] = R[p]
    for i in sorted(I.keys())[::-1]:
        T = T[0:i] + I[i] + T[i:]
    G[OT] = T
    return G[OT]

@profile
def part1() -> int:
    global ADVENTDAY, test, pp, C, maxX, maxY
    M = defaultdict(int)
    A = []
    T = lines[0]
    R = defaultdict(str)
    for line in lines[1:]:
        if line == "":
            continue
        p,i = line.split('->')
        p = p.strip()
        i = i.strip()
        R[p] = i
    for x in range(0,30):
        #print(f"Step {x+1}")
        T = calc(T, R)
#        for p,i in R:
#            if p in T:
#                loc = T.find(p)
#                I[loc+1] = i
#        for i in sorted(I.keys())[::-1]:
#            c = I[i]
#            print(T)
#            print(f"{i},{c}")
#            T = T[0:i] + c + T[i:]
#        z = 0
#        for i in sorted(I.keys()):
#            c = I[i]
#            print(T)
#            print(f"{i},{c}")
#            T = T[0:i+z] + c + T[z+i:]
#            z += 1
        print(f"Step {x+1}")
    print(len(T))
    c = defaultdict(int)
    for x in T:
        c[x] += 1
    return max(c.values()) - min(c.values())

#print(part2())


G = defaultdict(int)
@profile
def part2() -> int:
    global ADVENTDAY, test, pp, C, maxX, maxY
    M = defaultdict(int)
    T = lines[0]
    offset = defaultdict(int)
    offset.update(Counter(T))
    R = defaultdict(str)
    for line in lines[1:]:
        if line == "":
            continue
        p,i = line.split('->')
        p = p.strip()
        i = i.strip()
        R[p] = i
    pp(R)
    for i in range(0, len(T)-1):
        M[T[i:i+2]] += 1
    pp(M)
    pp(offset)
    if test:
        Y = 10**6
    else:
        Y = 10**6
    for x in range(0,Y):
        print(f"Round {math.log(x+1, 10)}")
        print(f"Round {x+1}")
        N = copy(M)
        for p in M.keys():
            if p in R:
                p1 = p[0] + R[p]
                p2 = R[p] + p[1]
                #print(f"{p1}, {p2}")
                w = M[p]
                N[p1] += w 
                N[p2] += w 
                offset[R[p]] += w
                N[p] -= w
        M = N
        #pp(M)

    pp(offset)
    print('=' * 40)
    pp(offset.values())
    return max(offset.values()) - min(offset.values())


#@profile
#def part2():
#    return 0 


print("Part 2:")
print(part2())
























