#!/usr/bin/env pypy3

import re
import json
import sys
import time
import heapq as hq
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


ADVENTDAY="18"
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

def add(p1,p2):
    return [p1,p2]


def addToNearest(p1: list, leftRem: int, rightRem: int):
    print(f"p1 = {p1}, leftRem = {leftRem}, rightRem = {rightRem}")
    if rightRem > 0:
        if isinstance(p1[1], list):
            p1[1] = addToNearest(p1[1], rightRem, leftRem)
        elif isinstance(p1[1], int):
            p1[1] += rightRem
            rightRem = 0
    if leftRem > 0:
        #print(f"p1[0] = {p1[0]}")
        if isinstance(p1[0], list):
            p1[0] = addToNearest(p1[0], rightRem, leftRem)
        elif isinstance(p1[0], int):
            p1[0] += leftRem 
            leftRem = 0
    #print(p1)

def explode(p1: list, level: int = 1, didExplode=False):
    print(f"p1 = {p1}")
    inner = p1
    leftRem = 0
    rightRem = 0
    if level >= 4:
        if isinstance(p1[0], list):
            print(f"p1[0] = {p1[0]}")
            print(f"p1[1] = {p1[1]}")
            #p1[1] += p1[0][1] 
            addToNearest(p1, p1[0][1], 0)
            #rightRem = copy(p1[0][0])
            print(f"p1 = {p1}")
            leftRem = copy(p1[0][0])
            p1[0] = 0
            return (p1, leftRem, rightRem, True)
        elif isinstance(p1[1], list):
            p1[0] += p1[1][0]
            #leftRem = copy(p1[1][1])
            rightRem = copy(p1[1][1])
            p1[1] = 0
            return (p1, leftRem, rightRem, True)
    if isinstance(inner[0], list):
        new, leftRem, rightRem, didExplode = explode(inner[0], level + 1)
        inner[0] = new
        if isinstance(inner[1], int):
            inner[1] += rightRem 
            rightRem = 0
        if level == 1 and rightRem > 0:
            addToNearest(inner[1], rightRem, 0)
    if isinstance(inner[1], list) and not didExplode:
        new, leftRem, rightRem, didExplode = explode(inner[1], level + 1)
        inner[1] = new
        if isinstance(inner[0], int):
            inner[0] += leftRem 
            leftRem = 0
    #print(f"{inner} | {leftRem} |  {rightRem}")
    if level == 1:
        return inner
    #if level == 4:
        #print(f"left = {leftRem}")
        #print(f"right = {rightRem}")
    return [inner, leftRem, rightRem, didExplode]


def split(p1: list, level: int = 1, didSplit = False):
    if isinstance(p1[0], list):
        split(p1[0])
    elif isinstance(p1[0], int):
        if p1[0] >= 10:
            new = [None,None]
            new[0] = math.floor(p1[0]/2)
            new[1] = math.ceil(p1[0]/2)
            p1[0] = new
            didSplit = True
    if didSplit:
        return
    if isinstance(p1[1], list):
        split(p1[1])
    elif isinstance(p1[1], int):
        if p1[1] >= 10:
            new = [None,None]
            new[0] = math.floor(p1[1]/2)
            new[1] = math.ceil(p1[1]/2)
            p1[1] = new
    return p1

assert explode([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
assert explode([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
assert explode([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
assert explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
assert explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]


a = add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1])
assert a == [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
assert explode(a) == [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
assert explode(explode(a)) == [[[[0,7],4],[15,[0,13]]],[1,1]]
b = explode(explode(a))
assert split(b) == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
assert split(split(b)) == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
b = split(split(b))
assert explode(b) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

@profile
def part1():
    global ADVENTDAY, test, pp, C, maxX, maxY, M
    M = defaultdict(int)
    l = [eval(x) for x in lines]
    s = l[0]
    for x in l[1:]:
        print(f"s = {s}")
        print(f"x = {x}")
        s = add(s, x)
        explode(s)
        split(s)
    print(s)

print(part1())

