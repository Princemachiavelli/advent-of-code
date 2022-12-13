#!/usr/bin/env python3

import re
import sys
import time
import statistics
import fractions
import sympy
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict
import itertools
from functools import partial
from collections import deque
#from advent import sirange, srange, nddict
import pprint
import math
import multiprocessing as mp 
from enum import Enum
from functools import cmp_to_key



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

def pp(stuff):
    print('-'*30)
    p = pprint.PrettyPrinter(indent=4, width=40, depth=3, compact=True)
    p.pprint(stuff)
    print('-'*30)

print(f"\n{'=' * 30}\n")

# Input parsing
input_start = time.time()
if stdin:
    lines: List[str] = [l.strip() for l in sys.stdin.readlines() if l.strip() != '']
else:
    with open(INFILENAME) as f:
        lines: List[str] = [l.strip() for l in f.readlines() if l.strip() != '']

input_end = time.time()

# Part 1
########################################################################################
print("Part 1:")


def test(p1,p2):
    print(f"Compare {p1} vs {p2}")
    if isinstance(p1, list):
        if isinstance(p2,list):
            if len(p1) > len(p2):
                return False
        if isinstance(p2, int):
            return test(p1,[p2])
    if isinstance(p2, list):
        if isinstance(p1, int):
            return test([p1], p2)
    for s1,s2 in zip(p1,p2):
        if isinstance(s1, int):
            if isinstance(s2, int):
                if s1 > s2:
                    return False
            elif isinstance(s2, list):
                if not test([s1], s2):
                    return False
        elif isinstance(s1, list) and isinstance(s2,list):
            if not test(s1,s2):
                return False

    return True

def test2(p1,p2, first=False, l=0):
    ind = "\t"*l
    print(f"{ind}- Compare {p1} vs {p2}")
    if p2 is None and p1 is not None:
        return (False, "ran out of items")
    if p1 is None and p2 is not None:
        return (True, "ran out of items")
    if isinstance(p1,int) and isinstance(p2,int):
        if p1 > p2:
            return (False, "is smaller")
        if p1 < p2:
            return (True, "is smaller")
        if p1 == p2:
            return None
    if isinstance(p1,int) and isinstance(p2, list):
        return test2([p1], p2)
    if isinstance(p1,list) and isinstance(p2, int):
        return test2(p1, [p2])
    if isinstance(p1,list) and isinstance(p2,list):
        for s1,s2 in itertools.zip_longest(p1,p2):
            print(f"{ind}- Compare2 {s1} vs {s2}")
            a = test2(s1,s2, False, l+1)
            if a is not None:
                return a
    return None 
        
def part1():
    A = []
    print(lines)
    for i in range(0,len(lines)-1,2):
        print(f"== Pair {(i/2)+1} ==")
        l1 = lines[i]
        l2 = lines[i+1]
        p1 = eval(l1)
        p2 = eval(l2)
        r,m = test2(p1,p2,True)
        if r:
            print(f"Left side {m}, so inputs are in the right order.")
            print(f"Adding {(i/2)+1}")
            A.append((i/2)+1)
        else:
            print(f"Right side {m}, so inputs are NOT in the right order.")

    print(A)
    AA = sum(A)
    print(f"ans = {AA}")

def cc(p1,p2):
    r,_ = test2(p1,p2)
    if r:
        r,_ = test2(p2,p1)
        if r:
            return 0
        return -1
    else:
        return 1
#part1()
#exit(0)
def part2():
    A = defaultdict(int)
    lines.append('[[2]]')
    lines.append('[[6]]')
    l2 = []
    for x in lines:
        l2.append(eval(x))
    l2 = sorted(l2, key=cmp_to_key(lambda p1,p2: cc(p1,p2)))
    AA = 1
    for i,x in enumerate(l2):
        if x == eval(lines[-1]) or x == eval(lines[-2]):
            AA *= (i+1)
        print(x)
    print(AA)
    exit(0)
    for i,x1 in enumerate(l2):
        for y,x2 in enumerate(l2):
            if i == y:
                continue
            r,_ = test2(x2,x1)
            if r:
                A[i] += 1
    #AA = 1
    #for i,v in A.items():
    #    if l2[i] == eval(lines[-1]) or l2[i] == eval(lines[-2]):
    #        AA *= (v+1)
    #    print(f"{l2[i]} : {v}")

    print(f"A = {AA}")
part2()
