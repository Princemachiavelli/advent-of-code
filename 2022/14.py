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

def parse(l):
    p = [x.strip() for x in l.split('->')]
    for i in range(len(p)-1):
        s1 = list(map(int,p[i].split(',')))
        s2 = list(map(int,p[i+1].split(',')))
        d1 = (1,-1)[s2[0] < s1[0]]
        d2 = (1,-1)[s2[1] < s1[1]]
        for x in range(s1[0],s2[0]+1*d1,d1):
            for y in range(s1[1],s2[1]+1*d2,d2):
                yield (x,y)


def part1():
    AA = 0
    Xmax = 0
    Xmin = 10000*10
    Ymax = 0
    M = defaultdict(lambda x: '.')
    for l in lines:
        for p in parse(l):
            x,y = p
            if Xmax < x:
                Xmax = x
            if x < Xmin:
                Xmin = x
            if Ymax < y:
                Ymax = y
            M[p] = '#'
    def gM():
        yMax = 0
        xMax = 0
        xMin = 10000*10
        for k,v in M.items():
            x,y = k
            if y > yMax:
                yMax = y
            if x > xMax:
                xMax = x
            if x < xMin:
                xMin = x
        return (xMax, yMax, xMin)
    orgY = gM()[1]
    print(f"floor = {orgY+2}")
    def prG(xMin,xMax):
        for y in range(orgY+3):
            for x in range(500-y,500+y+1):
                if (x,y) not in M:
                    M[(x,y)] = '.'
                #print(M[(x,y)], end='')
            #print('\n')
    def ct(s,e,y):
        if not e-s >= 0:
            return
        for x in range(s,e+1):
            M[(x,y)] = '#'
        ct(s+1,e-1,y+1)
    def fns():
        Z = dict()
        Z['#'] = 0
        Z['o'] = 0
        Z['.'] = 0
        r = 1
        for y in range(orgY+2):
            cb = 0
            for x in range(500-y,500+y+1):
                p = (x,y)
                if p not in M:
                    M[p] = '.'
                c = M[(x,y)]
                if c == '#':
                    cb += 1
                    Z['#'] += 1
                if c == '.' or c == 'o':
                    ct(x-cb,x-1,y)
                    cb = 0
                    if c == '.':
                        Z['.'] += 1
                    if c == 'o':
                        Z['o'] += 1
            ct(500+y-cb,500+y,y)
            cb = 0
            r += 2
        return Z
    #M[(500,0)] = '+'
    #for x in range(0,1000):
    #    y = gM()
    #    M[(x,y)] = '#'
    maxSand = 0
    r = 1
    for i in range(orgY+2):
        maxSand += r
        r += 2
    Z = fns()
    print(Z)
    print(f"end = {maxSand - Z['#']}")
    return maxSand - Z['#']
    for i in range(1,10000):
        xMax,yMax,xMin = gM()
        prG(xMin,xMax)
        print(f"maxSand = {maxSand}")
        #prG()
        #time.sleep(0.1)
        # sand at 500,0
        pos = (500,0)
        falling = True
        while falling:
            below = (pos[0], pos[1]+1)
            downLeft = (pos[0]-1, pos[1]+1)
            downRight = (pos[0]+1,pos[1]+1)
            #print(gM())
            xMax,yMax,xMin = gM()
            prG(xMin,xMax)
            Z = fns()
            print(Z)
            prG(xMin,xMax)
            print(maxSand)
            print(f"end2 = {maxSand - Z['#']}")
            return maxSand - Z['#']
            if below[1] >= orgY+2:
                for x in range(xMin-2,xMax+2):
                    M[(x,orgY+2)] = '#'
            if below not in M:
                M[below] = '.'
            if downLeft not in M:
                M[downLeft] = '.'
            if downRight not in M:
                M[downRight] = '.'
            if M[below] == '.':
                pos = below
            elif M[downLeft] == '.':
                pos = downLeft
            elif M[downRight] == '.':
                pos = downRight
            else:
                falling = False
        if pos[0] < xMin:
            xMin -= 2
        elif pos[0] > xMax:
            xMax += 2
        if not falling:
            print(f"sand stopped at {pos}")
            M[pos] = 'o'
        if pos == (500,0) and not falling:
            return i
    return -1

print(f"ans = {part1()}")

