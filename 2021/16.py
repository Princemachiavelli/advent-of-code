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


ADVENTDAY="16"
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


def toBin(ss):
    for s in ss:
        if s == '0':
            yield '0000'
        elif s == '1':
            yield '0001'
        elif s == '2':
            yield '0010'
        elif s == '3':
            yield '0011'
        elif s == '4':
            yield '0100'
        elif s == '5':
            yield '0101'
        elif s == '6':
            yield '0110'
        elif s == '7':
            yield '0111'
        elif s == '8':
            yield '1000'
        elif s == '9':
            yield '1001'
        elif s == 'A':
            yield '1010'
        elif s == 'B':
            yield '1011'
        elif s == 'C':
            yield '1100'
        elif s == 'D':
            yield '1101'
        elif s == 'E':
            yield '1110'
        elif s == 'F':
            yield '1111'
        else:
            print(f"WHATI IS {s}")
            yield "HELP"




class packet:
    version: int
    typeID: int
    children: list
    next: object 
    binary: str

    def __init__(self, binary: str):
        #print(f"binary = {binary}")
        self.binary = binary
        self.children = []
        V,T = self.parse()
        self.version = V
        self.typeID = T

    @classmethod
    def new(cls, binary: str):
        if(not all(x=='0' for x in binary)):
            return cls(binary)
        else:
            return None

    @staticmethod
    def fromHex(data: str):
        BIN = str(''.join(toBin(data)))
        return packet.new(BIN)

    def nextPacket(self):
        # Do I need to prevent it from parsing >1 packets?
        r = packet.new(self.binary)
        if r is None:
            self.binary = ''
        else:
            self.binary = r.getBinary()
        return r

    def getBinary(self):
        return self.binary

    def parse(self):
        BIN = self.binary
        V = int(BIN[0:3],2)
        T = int(BIN[3:6],2)
        BIN = BIN[6:]
        self.binary = BIN
        if T == 4:
            self.children.append(self.type4())
        else:
            self.typeO()
        return (V,T)

    def type4(self):
        BIN = self.binary
        lit = ''
        for x in range(0, len(BIN), 5):
            p = BIN[x]
            n = BIN[x+1:x+5]
            lit += n
            #print(f"{p}, {n} -> {lit}")
            if p == '0':
                self.binary = BIN[x+5:]
                break
        return int(lit,2)

    def typeO(self):
        BIN = self.binary
        #print(f"BIN= {BIN}")
        lengthTypeID = int(BIN[0])
        BIN = BIN[1:]

        if lengthTypeID == 0:
            l = int(BIN[0:15], 2)
            self.binary = BIN[15:]
            bb = self.binary[0:l]
            self.binary = self.binary[l:]
            #while (p := packet(bb)) and len(bb) > 1:
            while len(bb) > 1:
                #print(bb)
                if p := packet.new(bb):
                    self.children.append(p)
                    #bb = self.binary
                    bb = p.getBinary()
                else:
                    bb = ''
            #self.children.append(packet(self.binary[0:l]))
        elif lengthTypeID == 1:
            numSubPackets = int(BIN[0:11], 2)
            self.binary = BIN[11:]
            for _ in range(0, numSubPackets):
                #print(f"subpacket {_}")
                #print(self.binary)
                p = self.nextPacket()
                #bb = p.getBinary()
                #self.binary = p.getBinary()
                self.children.append(p)

    def asdict(self):
        #return {'version': self.version, }
        return vars(self)

    def __str__(self):
        s = f"version = {self.version}, typeID = {self.typeID} children = ["
        for c in self.children:
            s += ' '*5 + str(c)
        s += '\n]'
        return s

    def value(self):
        if self.typeID == 0:
            print("sum")
            return sum(self.getListValue())
        elif self.typeID == 1:
            print("prod")
            return math.prod(self.getListValue())
        elif self.typeID == 2:
            return min(self.getListValue())
        elif self.typeID == 3:
            return max(self.getListValue())
        elif self.typeID == 4:
            assert len(self.children) == 1
            return int(self.children[0])
        elif self.typeID == 5:
            assert len(self.children) == 2
            return int(self.children[0].value() > self.children[1].value())
        elif self.typeID == 6:
            assert len(self.children) == 2
            return int(self.children[0].value() < self.children[1].value())
        elif self.typeID == 7:
            assert len(self.children) == 2
            return int(self.children[0].value() == self.children[1].value())

    def getList(self):
        yield self
        for x in self.children:
            if isinstance(x, packet):
                yield from x.getList()
            else:
                yield x
    
    def getListValue(self):
        #yield self.value()
        for x in self.children:
            yield x.value()
        #    if isinstance(x, packet):
        #        #yield from x.getListValue()
        #        yield x.value()
        #    else:
        #        yield x

@profile
def part1():
    global ADVENTDAY, test, pp, C, maxX, maxY, M
    M = defaultdict(int)
    #data = bytes.fromhex(lines[0]).decode('ascii')
    #print(data)
    HEX = lines[0]
    Z = packet.fromHex(HEX)
    pp(str(Z))
    T = 0
#    for x in Z.getList():
#        if isinstance(x, packet):
#            T += x.version
    V = 0
    return Z.value()

#print(packet.fromHex('38006F45291200').children[0].children[0] == 10)
#print(packet.fromHex('38006F45291200').children[1].children[0] == 20)
#print(packet.fromHex('EE00D40C823060').children[0].children[0] == 1)
#print(packet.fromHex('EE00D40C823060').children[1].children[0] == 2)
#print(packet.fromHex('EE00D40C823060').children[2].children[0] == 3)
#print(packet.fromHex('EE00D40C823060'))

assert packet.fromHex('C200B40A82').value() == 3
assert packet.fromHex('04005AC33890').value() == 54
assert packet.fromHex('880086C3E88112').value() == 7
assert packet.fromHex('CE00C43D881120').value() == 9
assert packet.fromHex('D8005AC2A8F0').value() == 1
assert packet.fromHex('F600BC2D8F').value() == 0
assert packet.fromHex('9C005AC2F8F0').value() == 0
assert packet.fromHex('9C0141080250320F1802104A08').value() == 1

print(part1())
G = defaultdict(int)
@profile
def part2() -> int:
    return 0 


#print("Part 2:")
#print(part2())
























