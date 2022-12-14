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


ADVENTDAY="05"
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
    lines: List[str] = [l for l in sys.stdin.readlines()]
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l for l in f.readlines()]

input_end = time.time()

# Part 1
########################################################################################
print("Part 1:")

def parse():
    S = [[] for _ in range(0,20)]
    for l in lines:
        if l.strip() == '':
            break
        for i,c in enumerate(l):
            if c.isalpha():
                print(l)
                row = int((i-1)/4)
                print(f"{c} in col {i} is group {row}")
                S[row].append(c)
    return S

def parseRule(r):
    b = r.split()
    num = int(b[1])
    src = int(b[3]) - 1
    dst = int(b[5]) - 1
    return (num,src,dst)

def part1():
    N = 0
    M = parse()
    print(M)
    for l in lines:
        if l.count("move") == 0:
            continue
        num,src,dst = parseRule(l)
        #M[dst].insert(0,M[src][0])
        M[dst] = M[src][0:num] + M[dst]
        #del(M[src][0])
        del(M[src][0:num])
        print(M)
    print(M)
    A = ''
    for x in M:
        if len(x) != 0:
            A += x[0]
    print(A)
    print(f"total = {N}")

part1()


def part2():
    print()

#part2()
