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


ADVENTDAY="10"
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


def part1():
    A = 0 
    X = defaultdict(lambda x: 0)
    C = 0
    X[C] = 1
    for l in lines:
        if "noop" in l:
            X[C+1] = X[C]
            C += 1
        elif "addx" in l:
            _,n = l.split()
            n = int(n)
            print(f"C = {C} n = {n} X = {X[C]}")
            X[C+1] = X[C]
            print(f"C+1 = {C+1} n = {n} X = {X[C+1]}")
            #X[C+2] = (X[C+1] + n)
            X[C+1.5] = X[C+1]
            X[C+2] = X[C] + n
            print(f"C+2 = {C+2} n = {n} X = {X[C+2]}")
            #X[C+3] = X[C+2]
            #print(f"C+3 = {C+3} n = {n} X = {X[C+3]}")
            #C += 3
            C += 2
        else:
            print("Broken!")
    print(X)
    A = 0
    R = [copy(['.' for _ in range(40)]) for _ in range(6)]
    for c,v in X.items():
        if int(c) == c and c-0.5 in X:
            continue
        c = int(c+0.5)
        cn = c % 40 -1
        rn = int(c/40)
        print(f"c ={c}, v = {v}, cn = {cn}, rn = {rn}")
        if abs(cn-v) < 2:
            print("wrote to row")
            R[rn][cn] = '#' 
            print(''.join(R[rn]))

    for r in R:
        rr = ''.join(r)
        print(rr)
    return 0
    for i in [20,60,100,140,180,220]:
        print(A)
        if (i - 0.5) in X:
            print(X[i-0.5])
            A += X[i-0.5]*i
        else:
            print(X[i])
            A += X[i]*i
    print(f"ans = {A}")

part1()


def part2():
    print()

#part2()
    #return h > max(RB) or h > max(RA) or h > max(CB) or h > max(CA)
