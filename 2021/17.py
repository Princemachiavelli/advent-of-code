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

V = set()
N = defaultdict(int)
A = defaultdict(int)
def path(k):
    global V, M, S, G
    n = defaultdict(int)
    for r1,c1 in [(-1,0),(0,-1),(+1,0),(0,+1)]:
        rn = r1+k[0]
        cn = c1+k[1]
        if (rn,cn) not in V:
            n[(rn,cn)] = M[(rn,cn)]
    ne = min(n.items(), key=n.get)
    N[(rn,cn)] = ne


def solve2(graph, visited, start, end):
    dist = {}
    for i in visited.keys():
        visited[i] = float("inf")

    dist[start]=0
    d=graph.copy()
    while d:
        mn = None
        for node in M.keys():
            if not mn:
                mn = node
            elif dist[node] < dist[node]:
                mn = node
        for child, cost in graph[mn].items():
            if dist[mn] + cost < dist[child]:
                dist[child] = dist[mn] + cost
        d.pop(mn)
    return dist

            #s[(rn,cn)] = M[(rn,cn)]
def solve(graph,visited,a,b): #a start vertex, b end vertex
    dist={}
    for node in visited:
        dist[node]=float("inf")
    dist[a]=0
    d=graph.copy()
    while d:
        mn=None
        for node in d: # finding closest vertex
            if not mn:
                mn=node
            elif dist[node]<dist[mn]:
                mn=node
        for child,cost in graph[mn].items(): #updating distance 
            if dist[mn]+cost<dist[child]:
                dist[child]=dist[mn]+cost
        d.pop(mn) # removing mn as we updated distance wrt this vertex
    return dist

def path2():
    n = int(input()) #number of vertices
    graph = {}
    visited={}
    for i in range(n):
        u=input()
        graph[u]={}
        visited[u]=0
    e = int(input())
    for i in range(e):
        u, v, t = map(str, input().split()) # t is cost(must be positive)
        graph[u][v]=int(t)
    a = input()
    b = input()
    print(solve(graph,visited, a, b))

def neighbors(G, k):
    for r1,c1 in [(-1,0),(0,-1),(+1,0),(0,+1)]:
        rn = r1+k[0]
        cn = c1+k[1]
        if rn < 0 or cn < 0:
            continue
        if (int(rn/5),int(cn/5)) in G:
            yield (rn,cn)


def risk(M, p):
    n = M[p]
    return n

@profile
def dijkstra(G, s, e):
    n = len(G)
    #visited = [False]*n
    visited = defaultdict(int)
    weights = defaultdict(float)
    for r,c in G.keys():
            visited[(r, c)] = False
            weights[(r, c)] = math.inf
    path = defaultdict(int)
    queue = []
    weights[s] = 0
    hq.heappush(queue, (0, s))
    i = 0
    while len(queue) > 0:
        g, u = hq.heappop(queue)
        #pp(f"g,u = {g} {u}")
        visited[u] = True
        for v in neighbors(G, u):
            #pp(f"neighbor = {v}")
            w = risk(G, v)
            #pp(f"neighbor = {v}, {w}")
            #pp(f"visited[v] = {visited[v]}")
            if not visited[v]:
                f = g + w
                #pp(f"f = {g}+{w}")
                if f < weights[v]:
                    weights[v] = f
                    #path.append(u)
                    path[i] = u
                    hq.heappush(queue, (f, v))

        i += 1
    #pp(path)
    #pp(weights)
    return path, weights


def pg(M, P=[]):
    pp(P)
    maxC = 0
    maxR = 0
    for k in M.keys():
        #print(f"k = {k}")
        r = k[0]
        c = k[1]
        if r > maxR:
            maxR = r
        if c > maxC:
            maxC = c
    for r in range(0,maxR+1):
        s = ''
        for c in range(0, maxC+1):
            if (r,c) in P:
                s += '|'
            s += str(M[(r,c)])
            if (r,c) in P:
                s += '|' 
        print(s)


def risk2(p: int, e: int):
    return int((p+1)/(e+0.0001))


def move(S, V):
    vx = V[0]
    vy = V[1]
    ax = S[0] + vx
    ay = S[1] + vy
    if vx > 0:
        vx += -1
    elif vx < 0:
        vx += 1
    vy += -1
    return ((ax,ay),(vx,vy))

def inTarget(S, target):
    x = S[0]
    y = S[1]
    if x >= int(target[0]) and x <= int(target[1]):
        if y >= int(target[2]) and y <= int(target[3]):
            #print(f"{x},{y} in {target}...")
            return True
    #print(f"{x},{y} not in {target}...")
    return False

def belowTarget(S, target):
    x = S[0]
    y = S[1]

    if x > int(target[2]):
        return True
    #if x > int(target[2]) and y < int(target[2]):
    #    return True
    return False


def getMinX(x: int): 
    return int(0.5*((8*x+1)**0.5 - 1))

def getYValue(vy: int, steps: int):
    T = 0
    for x in range(0,steps):
        T += vy - (x*-1)
    return T

assert getMinX(10) == 4
assert getMinX(15) == 5


def add(p1, p2):
    new = [p1,p2]

@profile
def part1():
    global ADVENTDAY, test, pp, C, maxX, maxY, M, lines
    M = defaultdict(int)
    l = [eval(x) for x in lines]
    print(l[0])

    print('-'  * 30)
    return 0 

print(part1())

@profile
def part2():
    return 0

#print(part2())
























