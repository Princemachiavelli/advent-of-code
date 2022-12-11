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
#from advent import sirange, srange, nddict
import pprint
import math


ADVENTDAY="11"
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


def parse(ll):
    N = None
    I = None
    O = None
    T = None
    TT = None
    TF = None
    for l in ll:
        if "Monkey" in l:
            N = l.split()
            N = int(N[-1].split(':')[0])
        elif "Starting items" in l:
            I = l.split(':')
            I = [int(x) for x in I[-1].split(',')]
        elif "Operation" in l:
            O = eval('lambda old: ' + l.split('=')[-1])
        elif "Test" in l:
            T = int(l.split()[-1])
        elif "If true" in l:
            TT = int(l.split()[-1])
        elif "If false" in l:
            TF = int(l.split()[-1])


    return {
            'number':N,
            'items':I,
            'op':O,
            'test':T,
            'true': TT,
            'false': TF,
            'numinspect': 0
            }
def test(M, dv):
    if len(M['items']) == 0:
        return None
    old = M['items'][0]
    del(M['items'][0])
    #print(f"Monkey inspects item with level {old}")
    old = old % dv
    new = M['op'](old)
    #print(f"Worry level becomes {new}")
    #new = int(new / 3)
    tresult = new % M['test'] == 0
    #print(f"test = {tresult}")
    M['numinspect'] += 1
    if tresult:
        #new = old
        return (new, M['true'])
    else:
        #new = old
        return (new, M['false'])

def part1():
    A = 0 
    W = defaultdict(lambda x: 0)
    M = []
    for i in range(0,len(lines),7):
        MR = parse(lines[i:i+7])
        M.append(MR)
        print(MR)
    dv = 1
    L = []
    for x in M:
        dv *= x['test']
        pt = sympy.isprime(x['test'])
        print(f"{x['test']} prime test is {pt}")
        L.append(x['test'])
    print(L)
    dv = math.lcm(*L)
    print(dv)
    return dv
    for ri in range(1,10000+1):
        print(f"Round {ri}")
        for mk in M:
            #print(f"Monkey {mk['number']}")
            for _ in range(len(mk['items'])):
                R = test(mk, dv)
                if R is None:
                    continue
                M[R[1]]['items'].append(R[0])
        #if ri % 100 == 0:
        #    TI = 0
        #    for mk in M:
        #        TI += mk['numinspect']
        #    for mk in M:
        #        print(f"{mk['number']} = {mk['numinspect'] * 10000/ri}")
    L = []
    for x in M:
        L.append(x['numinspect'])
        print(L)
    L = sorted(L)
    print(L[-2:])
    A = L[-2] * L[-1]
    print(f"ans = {A}")

part1()
