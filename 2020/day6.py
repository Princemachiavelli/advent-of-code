#!/usr/bin/env nix-shell
#! nix-shell -i "poetry run pypy3" -p pypy3 poetry

import advent_of_code_py as ac
from copy import copy

@ac.solve(2020,6,1, session_list=["s2021"])
def part1(data = None):
    curSum = 0
    print(data)
    for group in data.split("\n\n"):
        group = group.strip().replace('\n', '')
        print(group)
        print(set(list(group)))
        print("-----")
        curSum += len(set(list(group)))
    return curSum

#part1()

@ac.solve(2020,6,2, session_list=["s2021"])
def part2(data = None):
    curSum = 0
    print(data)
    for group in data.split("\n\n"):
        print("-----")
        print(group)
        ss = None 
        for persons in group.strip().split("\n"):
            if ss == None:
                ss = set(persons)
            else:
                ls = set(persons)
                ss = ss.intersection(ls)
        print(ls)
        print(ss)
        print("-----")
        curSum += len(ss)
    return curSum

part2()
