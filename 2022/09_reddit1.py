#!/usr/bin/env python3
rope = [0] * 10
seen = [set() for _ in range(10)]
dirs = {'L':+1, 'R':-1, 'D':1j, 'U':-1j}
sign = lambda x: x and (1, -1)[x<0]
for line in open(0):
    d, n = line.split()
    for _ in range(int(n)):
        rope[0] += dirs[d]
        for i in range(1, 10):
            diff = rope[i-1] - rope[i]
            if abs(diff) >= 2:
                rope[i] += complex(sign(diff.real), sign(diff.imag))
            seen[i].add(rope[i])
print(len(seen[1]), len(seen[9]))
