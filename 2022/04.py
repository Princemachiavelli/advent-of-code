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


ADVENTDAY="04"
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
    N = 0
    for l in lines:
        print(l)
        p1,p2 = l.split(',')
        print(f"p1 = {p1}, p2={p2}")
        s1 = [int(x) for x in p1.split('-')]
        s2 = [int(x) for x in p2.split('-')]
        w1 = set(range(s1[0],s1[1]+1))
        w2 = set(range(s2[0],s2[1]+1))
        if len(w1.intersection(w2)) > 0:
            N += 1
            #print(','.join([str(x) for x in s1]))
            #print(','.join([str(x) for x in s2]))
            print("YES")
        elif len(w2.intersection(w1)) > 0:
            N += 1
            print("YES")
    print(f"total = {N}")

part1()


def part2():
    print()

#part2()
