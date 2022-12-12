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
from itertools import repeat
from functools import partial
from collections import deque
#from advent import sirange, srange, nddict
import pprint
import math
import multiprocessing as mp 



ADVENTDAY="12"
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
def validMoves(B, L, xMax, yMax):
    M = [ (-1,0), (1,0), (0,-1), (0,1)]
    for d in M:
        nX = L[0] + d[0]
        nY = L[1] + d[1]
        #if nX < 0 or nY < 0 or nX >= xMax or nY >= yMax:
        #    continue
        # (col, row)
        nL = (nX, nY)
        if nL not in B:
            continue
        nO = B[nL]
        oO = B[L]
        if ord(nO) - ord(oO) <= 1:
            yield nL
def parse(ll):
    B = dict()
    S = None
    E = None
    xMax = len(ll[0])
    yMax = len(ll)
    lowest = []
    for r,l in enumerate(ll):
        for c,cc in enumerate(l):
            if cc == 'a':
                lowest.append((c,r))
            # (col, row)
            B[(c,r)] = cc
            if cc == 'S':
                B[(c,r)] = 'a'
                S = (c,r)
            if cc == 'E':
                B[(c,r)] = 'z'
                E = (c,r)
    return (B,S,E, xMax, yMax, lowest)
def part1():
    B,S,E,xMax,yMax,lowest = parse(lines)
    print((xMax,yMax))
    C = S
    print(f"Starting pos = {C}")
    #print(B)
    LM = None
    def dfs(L,B,E,M=set(), LM=None, V=set()):
        V.add(L)
        #print(len(M))
        #print(L)
        if LM is not None and len(M) > len(LM):
            pass
        elif L == E:
            #print(M)
            #print(f"{L} is the end {E}")
            #print(f"{len(M)}")
            if LM is not None and len(LM) > len(M):
                LM = M
            elif LM is None:
                LM = M
            yield len(M)
        elif LM is not None and len(M) > len(LM) and L == E:
            pass
        else:
            vm = validMoves(B,L,xMax,yMax)
            for vd in vm:
                if vd in M or vd in V:
                    continue
                else:
                    #print(M)
                    #print(f"trying next cell: {vd}")
                    #M.append(vd)
                    M.add(vd)
                    #######nBL = BL.union(set(vm))
                    #print(f"nBL = {nBL}")
                    yield from bfs(vd,B,E,M,LM,V)
                    #del(M[-1])
                    M.remove(vd)
    def bfs(C,B,E):
        q = deque()
        V = set()
        q.append((C,0))
        while q:
            n,cost = q.popleft()
            if n in V:
                continue
            V.add(n)
            if n == E:
                return cost
            for nb in validMoves(B,n,xMax,yMax):
                #if nb not in V:
                q.append((nb, cost+1))
        return 10**9
        print(len(V))
    MS = None
    for sc in lowest:
        aa = bfs(sc,B,E)
        if MS is None or aa < MS:
            MS = aa
    A = MS
    print(f"ans = {A}")

part1()
