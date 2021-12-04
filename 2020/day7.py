#!/usr/bin/env nix-shell
#! nix-shell -i "poetry run pypy3" -p pypy3 poetry

import advent_of_code_py as ac
from itertools import chain
from copy import copy

treeMap = dict()

data1 = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""
def parseData(data: str):
    global treeMap
    for line in data.split("\n"):
        if len(line) == 0:
            continue
        parts = [x.strip() for x in line.replace("bags contain", ",").replace("no other", '').replace("bags",'').replace("bag",'').replace('.','').split(',')]
        parentName = parts[0]
        if parentName not in treeMap:
            treeMap[parentName] = dict()
        children = list()
        for c in parts[1:]:
            if len(c) == 0:
                continue
            parts = c.split(' ')
            count = int(parts[0])
            name = ' '.join(parts[1:])
            name = name.strip()
            treeMap[parentName][name] = count

def followTree(start: str):
    global treeMap
    a = []
    if start in treeMap:
        for c,n in treeMap[start].items():
            yield c
            yield from followTree(c)
    else:
        yield []

def followTree2(start: str, mult=1):
    global treeMap
    if start in treeMap:
        for c,n in treeMap[start].items():
            yield (c,n*mult)
            yield from followTree2(c, n*mult)

def countTree(target: str)->list:
    global treeMap
    validColors = []
    for k in treeMap.keys():
        if k == target:
            continue
        termColors = followTree(k)
        for x in termColors:
            if target in x:
                validColors.append(k)
    return validColors 

@ac.solve(2020,7,1, session_list=["s2021"])
def part1(data = None):
    global treeMap, data1, a
    data1 = data
    parseData(data)
    key = "shiny gold"
    a = countTree(key)
    #for c in a:
    #    print(followTree2(c))
    #print(len(a))
    return len(set(a))

def part2(data='shiny gold'):
    count = 0
    print(data)
    for k,v in followTree2(data):
        count += int(v)
    return count

part1()
part2()
