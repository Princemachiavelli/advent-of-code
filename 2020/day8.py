#!/usr/bin/env nix-shell
#! nix-shell -i "poetry run pypy3" -p pypy3 poetry

import advent_of_code_py as ac
from itertools import chain
from copy import copy,deepcopy


def parseLine(line: str):
    op, num = line.split(" ")
    op = op.strip()
    num = int(num.strip())
    return (op, num)

def passbyval(func):
    def new(*args):
        cargs = [deepcopy(arg) for arg in args]
        return func(*cargs)
    return new

@passbyval
def runCode(start: int, acc: int, lines, ranCode=set(), swapLine = None):
    i = start
    if swapLine != None:
        op, num = parseLine(lines[swapLine])
        if op == "nop":
            lines[swapLine] = f"jmp {num}"
        elif op == "jmp":
            lines[swapLine] = f"nop {num}"
        else:
            print("Not a valid line to switch")
    while True:
        if i in ranCode and i != len(lines)-1:
            print(lines[i-1:i+1])
            yield (False, swapLine, acc, i)
            break
        op, num = parseLine(lines[i])
        if op == "acc":
            acc += num
            ranCode.add(i)
            i += 1
        elif op == "jmp":
            if swapLine is None:
                yield from runCode(i, acc, lines, ranCode, i) 
            ranCode.add(i)
            i += num
            continue
        elif op == "nop":
            if swapLine is None:
                yield from runCode(i, acc, lines, ranCode, i) 
            ranCode.add(i)
            i += 1
        if i >= len(lines)-1:
            print("Reached end of file")
            yield (True, swapLine, acc, i)
            break

@ac.solve(2020,8,1, session_list=["s2021"])
def part1(data):
    global acc
    global lines
    acc = 0
    lines = data.split('\n')
    ranCode = set()
    i = 0
    while True:
        print(i)
        print(ranCode)
        if len(lines[i]) == 0:
            continue
        print(lines[i])
        ranCode.add(i)
        op, num = lines[i].split(" ")
        op = op.strip()
        num = int(num.strip())
        if op == "acc":
            print(f"acc {acc}")
            acc += num
        elif op == "jmp":
            i += num
            continue
        i += 1

    return acc

@ac.solve(2020,8,2, session_list=["s2021"])
def part2(data):
    global acc
    acc = 0
    lines = data.split('\n')[:-1]
    print(len(lines))
    print(lines[len(lines)-1])
    result = runCode(0,0,lines,set(),None)
    return list(result)

#part1()
part2()
