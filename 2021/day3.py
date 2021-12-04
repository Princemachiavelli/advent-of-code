#!/usr/bin/env python3.9

#!/usr/bin/env nix-shell
#! nix-shell -i "poetry run python3.10" -p pypy3 poetry python3.9
import copy
import advent_of_code_py as ac

posX = 0
posY = 0
aim = 0

def printMap():
    global map1
    for r in map1:
        print(''.join(r))

def isPosTree(x: int, y: int):
    global map1
    maxRight = len(map1[0])
    x = x % maxRight
    # The map repeats to the right so need to wrap X pos
    if map1[-1*y][x] == "#":
        map1[-1*y][x] = "X"
        return True
    map1[-1*y][x] = "O"
    return False

def countTrees(text: str, mX: int, mY: int):
    global map1, posX, curY
    posX = 0
    curY = 0
    map1 = translateMap(text)
    countTrees = 0
    while -1 * curY < len(map1) + mY:
        movePos(mX, mY)
        if isPosTree(posX, curY):
            countTrees += 1
    return countTrees

def reset():
    global posX, posY, aim
    posX = 0
    posY = 0
    aim = 0

def splitOnEmptyLines(line: str, removeEmpty = True) -> list:
    for x in line.split("\n\n"):
        if removeEmpty and len(x) == 0:
            continue
        yield x

def movePos2(command: str) -> str:
    global posX, posY, aim
    direction, magnitude = command.split(" ")
    m = int(magnitude)

    if direction == "forward":
        posX += m
        posY += aim * m
    elif direction == "down":
        aim += m
    elif direction == "up":
        aim -= m

def calcPos(input1: str):
    reset()
    input1 = input1.strip()
    for l in input1.splitlines():
        if len(l) == 0:
            continue
        movePos2(l)
    return posX * posY


data1 = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


@ac.solve(2021,3,1, session_list=["s2021"])
def part1(data = None):
    commonBit = {}
    for line in data.split("\n"):
        if len(line) == 0:
            continue
        for x in range(0, len(line)):
            if x not in commonBit:
                # 0,1s
                commonBit[x] = 0
            bit = line[x]
            if bit == "0":
                commonBit[x] -= 1
            if bit == "1":
                commonBit[x] += 1
    s = ""
    s2 = ""
    for i,bit in commonBit.items():
        if bit > 0:
            s = s + "1"
            s2 = s2 + "0"
        elif bit < 0:
            s = s + "0"
            s2 = s2 + "1"
        else:
            print("BAD")
    gamma = int(s,2)
    esp = int(s2,2)
    print(gamma*esp)

reset()

def getOG(data = None):
    commonBit = {}
    for line in data.split("\n"):
        if len(line) == 0:
            continue
        for x in range(0, len(line)):
            if x not in commonBit:
                # 0,1s
                commonBit[x] = 0
            bit = line[x]
            if bit == "0":
                commonBit[x] -= 1
            if bit == "1":
                commonBit[x] += 1
    s = ""
    s2 = ""
    for i,bit in commonBit.items():
        if bit > 0:
            s = s + "1"
            s2 = s2 + "0"
        elif bit < 0:
            s = s + "0"
            s2 = s2 + "1"
        else:
            s += "S"
            s2 += "S"
    gamma = s 
    esp = s2
    return(gamma, esp)



def old():
    for i,v in enumerate(pos):
        for p in range(0, len(v)):
            gamma1, esp1 = getOG('\n'.join(list(posOX)))
            gamma2, esp2 = getOG('\n'.join(list(posGA)))
            gamma = gamma1
            esp = esp2
            print(gamma)
            print(esp)
            if v[p] != gamma[p] and v in posOX and len(posOX) > 0:
                posOX.remove(v)
            if v[p] != esp[p] and v in posGA and len(posGA) > 0:
                posGA.remove(v)
            if gamma[p] == "S" and v[p] != 1 and v in posOX and len(posOX) > 0:
                posOX.remove(v)
            if esp[p] == "S" and v[p] != 0 and v in posGA and len(posGA) > 0:
                posGA.remove(v)

@ac.solve(2021,3,2, session_list=["s2021"])
def part2(data = None):
    gamma, esp = getOG(data)
    posOX = set()
    posGA = set()
    for line in data.split("\n"):
        if len(line) == 0:
            continue
        posOX.add(line)
        posGA.add(line)
        pos = copy.copy(posOX)
        lastGA = ""
    example = list(posOX)[0]
    for p in range(0, len(example)):
            gamma1, esp1 = getOG('\n'.join(list(posOX)))
            gamma2, esp2 = getOG('\n'.join(list(posGA)))
            gamma = gamma1
            esp = esp2
            print(gamma)
            for v in copy.copy(posOX):
                if len(posOX) == 1:
                    break
                if gamma[p] == "S" and v[p] != "1":
                    posOX.remove(v)
                elif gamma[p] == "S":
                    continue
                elif v[p] != gamma[p] and len(posOX) > 0:
                    posOX.remove(v)
            for v in copy.copy(posGA):
                if len(posGA) == 1:
                    break
                if esp[p] == "S" and v[p] != "0": 
                    posGA.remove(v)
                elif esp[p] == "S":
                    continue
                elif v[p] != esp[p] and len(posGA) > 0:
                    posGA.remove(v)
    print(posOX)
    print(posGA)
    return int(list(posOX)[0],2) * int(list(posGA)[0],2)

part2()
