#!/usr/bin/env pypy3

import re
import sys
import time
import statistics
from typing import List, Match, Optional
from copy import copy, deepcopy
from collections import defaultdict
from itertools import repeat
from functools import partial
from advent import sirange, srange, nddict
import pprint
import math
from astar import * 
if type(__builtins__) is not dict or 'profile' not in __builtins__: profile=lambda f:f;
sys.setrecursionlimit(10000000)


ADVENTDAY="08"
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

def cost(x,y):
    return sum(range(1,abs(x-y)+1))

def l2(x: list, p: int = 2):
    return sum(abs(y)**p for y in x)**(1/p)

def pm(x: list):
    return 1/len(x)*sum(x)

D = dict()
def ident(s: str):
    S = sorted(set(s))
    EI = set('a,b,c,d,e,f,g')
    NINE = set('a,b,c,d,f,g')
    if S == (EI):
        return 8
    elif S == EI - set(['e']):
        return 9
    elif S == EI - set(['b','e','d','g']):
        return 7
    elif S == EI - set(['c']):
        return 6
    elif S == EI - set(['c','e']):
        return 5
    elif S == EI - set(['a','e', 'g']):
        return 4
    elif S == EI - set(['b','e']):
        return 3
    elif S == EI - set(['b', 'f']):
        return 2
    elif S == set(['c','f']):
        return 1
    elif S == EI - set('d'):
        return 0
    else:
        print("ERROR")
        print(S)

def ident2(s: str):
    S = sorted(set(s))
    EI = set('a,b,c,d,e,f,g'.split(','))
    #NINE = set('a,b,c,d,f,g'.split(','))
    NINE = set("cefabd")
    SEV = set("dab");
    print(f"len(NINE) = {len(NINE)}")
    if set(EI) == set("acedgfb"): 
        return 8
    elif set(NINE) == SEV.union():
        return 9
    elif set(SEV) == set("dab"): 
        return 7
    elif len(S) == len(EI - set(['c'])):
        return 6
    elif len(S) == len(EI - set(['c','e'])):
        return 5
    elif len(S) == len(EI - set(['a','e', 'g'])):
        return 4
    elif len(S) == len(EI - set(['b','e'])):
        return 3
    elif len(S) == len(EI - set(['b', 'f'])):
        return 2
    elif len(S) == len(set(['c','f'])):
        return 1
    elif len(S) == len(EI - set('d')):
        return 0
    else:
        print(S)


def ident3(A: str):
    B = defaultdict(str)
    for s in A.split():
        s = set(s)
        if len(s) == 3:
            B[7] = s
        elif len(s) == 4:
            B[4] = s
        elif len(s) == 2:
            B[1] = s
        elif len(s) == 8:
            B[8] = s
    return B



def part22():
    G = defaultdict(int)
    A = defaultdict(str)
    R = dict()
    for line in lines:
        x = line.split('|')
        d = x[1]
        b = ident3(d)
        print(b)
        A.update(b)
        print(line)
    R['top'] = A[7] - A[1]
    for line in lines:
        x = line.split('|')
        s = x[0]
        d = x[1]


D = defaultdict(list)


def initSol(line: str = None):
    D = defaultdict(list)
    if line == None:
        line = "abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg"
    c = line
    for w in c.split():
        for char in w:
            D[char].append(len(w))
#    for w in d.split():
#        for char in w:
#            D[char].append(len(w))
    print("letter by different lengths")
    for k,v in D.items():
        print(f"{k} = {sorted(set(v))}")
    print("letter by occurence in 1-10")
    for k,v in D.items():
        print(f"{k} = {len(v)}")
    print("letter by unique lengths")
    for k,v in D.items():
        print(f"{k} = {len(set(v))}")
    for k,v in D.items():
        print(f"{k} = {len(v), len(set(v))}")
    G = defaultdict(str)
    for k,v in D.items():
        G[(len(v), len(set(v)))] = k
    return G

def rr(a: str):
    sol = "abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg".split()
    for i,v in enumerate(sol):
        if set(a) == set(v):
            return i

def part23():
    global D
    D = initSol()
    Y = 0
    for line in lines:
        y = ""
        M = defaultdict(str)
        s,d = line.split('|')
        stats = initSol(s)
        for k,v in stats.items():
            M[v] = D[k]
        print(M)
        e = ""
        for c in d:
            if c in M:
                e += M[c]
            else:
                e += c
        print("For each word")
        for d in e.split():
            print(d)
            y += str(rr(d))
            print(y)
        Y += int(y)
    return Y

print(part23())
# [1, 4, 9]
def part1() -> int:
    global ADVENTDAY, test, pp
    G = defaultdict(int)
    for line in lines:
        x = line.split('|')
        s = x[0]
        d = x[1]
        for entry in d.split():
            print("size = " + str(len(entry)))
            r = ident2(entry)
            print(r)
            G[r] += 1
    print(G)
    return G[1] + G[4] + G[7] + G[8]

#print(part1())

D = defaultdict(int)

@profile
def c(f: int, d: int):
    global D
    if (f,d) in D:
        return D[(f,d)]
    if f > d or d == 0:
        D[(f,d)] = 1
        return 1
    if f == 0:
        D[(f,d)] = c(0, d - 7) + c(0, d - 9)
        return D[(f,d)]
    else:
        n = min(f,d)
        s = c(f-n,d-n)
        D[(f-n,d-n)] = s
        return s

@profile
def part2():
    return 0 


print("Part 2:")
#print(part2())
























