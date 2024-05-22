import sys
import math
import numpy as np
from PIL import Image

def read_instructions(filename):
    filename = sys.argv[1]
    lines = open(filename, 'r').readlines()
    ins = [line.strip().split(' ')[2][2:-1] for line in lines]
    ans = []
    for x in ins:
        u = int(x[-1])
        d = ['R', 'D', 'L', 'U'][u]
        v = int(x[:-1], 16)
        ans.append((d, v))
    return ans


def instructions_to_vertices(ins):
    ans = [[0,0]]
    count = 0
    for x in ins:
        z = ans[-1][:]
        d = x[0]
        s = x[1]
        count += s
        if d == 'R':
            z[1] += s
        if d == 'L':
            z[1] -= s
        if d == 'U':
            z[0] -= s
        if d == 'D':
            z[0] += s
        ans.append(z)
    m1 = min([x[0] for x in ans])
    m2 = min([x[1] for x in ans])
    ans = [[x[0]-m1, x[1]-m2] for x in ans]
    return ans[:-1], count

def shoelace_formula (verts):
    ans = 0
    for p1, p2 in zip(verts, verts[1:]):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        ans += x1 * y2 - x2 * y1
    return int(abs(ans/2))

ins = read_instructions(sys.argv[1])

verts, count = instructions_to_vertices(ins)

ans = shoelace_formula(verts=verts)
print(int(ans + count/2 + 1))
