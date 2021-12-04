#!/usr/bin/env python3

import sys
from collections import defaultdict
from functools import lru_cache

import advent_of_code_py as ac

@ac.solve(2020,7,1, session_list=["s2021"])
def part1(data=None):
    rules = data.split("\n")
    bags = defaultdict(dict)

    for rule in rules:
        if len(rule) == 0:
            continue
        parts = rule.split(' ')
        color = ' '.join(parts[:2])
        in_parts = ' '.join(parts[4:]).split(',')
        for part in in_parts:
            if not 'no other bags' in part:
                sp = part.strip().split(' ')
                bags[color][' '.join(sp[1:3])] = int(sp[0])
            else:
                bags[color] = {}

    def can_hold(in_color, out_color):
        if in_color in str(bags[out_color]):
            return True
        return any([can_hold(in_color, b)for b in bags[out_color]])

    #part1 = sum([can_hold('shiny gold', bag) for bag in bags])
    count = 0
    for bag in bags:
        if can_hold('shiny gold', bag):
            print(bag)
            count += 1
    return count 

part1()
