#!/usr/bin/env python3.9

#!/usr/bin/env nix-shell
#! nix-shell -i "poetry run python3.10" -p pypy3 poetry python3.9
from copy import copy, deepcopy
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


def buildBoard(data):
    board = []
    for line in data.split('\n'):
        if len(line) > 0:
            board.append([int(x.strip()) for x in line.replace('  ', ' ').replace('  ',' ').split(' ') if x != ''])
    return board

def parseData(data):
    groups = data.split('\n\n')
    numberOrder = [int(x.strip()) for x in groups[0].split(',')]
    boards = [buildBoard(x) for x in groups[1:]]
    return (numberOrder, boards)


def calcScore(nums, board):
    boardNums = list()
    for r in board:
        boardNums += r
    print(boardNums)
    print(nums)
    remain = set(boardNums) - set(nums)
    print(remain)
    print((sum(remain), nums[-1]))
    return sum(remain) * nums[-1]

def isBingo(nums, board):
    print(nums)
    for row in board:
        if len(set(row).intersection(set(nums))) >= len(set(row)):
            print(set(nums))
            print(set(row))
            return True
    for x in range(0, len(board)):
        column = set([board[x][y] for y in range(0,len(board[0]))])
        if len(set(column).intersection(set(nums))) >= len(column):
            print(column)
            return True
    return False


data3 ="""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""
@ac.solve(2021,4,1, session_list=["s2021"])
def part1(data = None):
    numOrder, boards = parseData(data)
    hasWon = set()
    for x in range(0, len(numOrder)):
        for i in range(0, len(boards)):
            b = boards[i]
            if isBingo(numOrder[0:x+1], b):
                hasWon.add(i)
                if len(hasWon) == len(boards) - 1:
                    return calcScore(numOrder[0:x+1], b)
    return False
print(part1())
