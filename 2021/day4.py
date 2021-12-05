#!/usr/bin/env python3.9

#!/usr/bin/env nix-shell
#! nix-shell -i "poetry run python3.10" -p pypy3 poetry python3.9
from copy import copy, deepcopy
import advent_of_code_py as ac

def buildBoard(data):
    board = []
    for line in data.split('\n'):
        if len(line) > 0:
            board.append([int(x.strip()) for x in line.split() if x != ''])
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
