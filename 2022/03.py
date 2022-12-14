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


ADVENTDAY="03"
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
    G = [0]*1000
    S = 0
    for i in range(0,len(lines), 3):
        group = lines[i:i+3]
        k = list(set(group[0]).intersection(group[1]).intersection(group[2]))[0]
        print(f"group size = {len(group)}")
        print(f"key = {k}")
        #s1 = set(c1)
        #s2 = set(c2)
        #both = list(s1.intersection(s2))
        if k.islower():
            S += ord(k) - ord('a') + 1
        else:
            S += ord(k) - ord('A') + 27
        print(f"S is now {S}")
    print(S)

part1()


def part2():
    print()

part2()
