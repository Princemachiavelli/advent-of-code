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
    S = 0
    M = defaultdict(int)
    K = []
    for l in lines:
        #print(l)
        if "$ cd" in l:
            p = l.split()[2]
            #print(f"cd to {p}")
            if p == '..':
                K = K[0:-1] 
            else:
                #print(f"adding to K {p}")
                K.append(p)
            #print(K)
        elif not l[0] == '$' and l[0:3] != 'dir':
            s,f = l.split()
            s = int(s)
            #print(f"{f} is {s} size")
            for i in range(0,len(K)+1):
                kk = ''.join(K[0:i])
                #print(kk)
                M[kk] += s
    S = 0
    print(M)
    NE = 30000000 - (70000000 - M['/'])
    Z = []
    for k,v in M.items():
        if v > NE:
            Z.append(v)
    A = min(Z)
    print(f"ans = {A}")

part1()


def part2():
    print()

#part2()
