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


ADVENTDAY="02"
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
    M = { "A": "X", "B": "Y", "C": "Z" }
    M2 = {
            "AX": "Z",
            "AY": "X",
            "AZ": "Y",
            "BX": "X",
            "BY": "Y",
            "BZ": "Z",
            "CX": "Y",
            "CY": "Z",
            "CZ": "X",
            }

    for l in lines:
        O,Y = l.split()
        L = O+Y
        if Y == "Z":
            S += 6
        elif Y == "Y":
            S += 3
        if M2[L] == "Y":
            S += 2
        elif M2[L] ==  "X":
            S += 1
        elif M2[L] == "Z":
            S += 3
        print(f"{O} : {Y} : {S}")
        
    print(S)


part1()


def part2():
    print()

part2()
