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
    for x in ins:
        z = ans[-1][:]
        d = x[0]
        s = x[1]
        if d == 'R':
            z[0] += s
        if d == 'L':
            z[0] -= s
        if d == 'U':
            z[1] -= s
        if d == 'D':
            z[1] += s
        ans.append(z)
    return ans[:-1]

def pair_overlaps (p1, p2):
    """ return true if pair overlaps on the row-axis """
    r11 = p1[0]
    r12 = p1[1]
    r21 = p2[0]
    r22 = p2[1]
    if r21 > r12 or r22 < r11:
        return False
    return True
    
def vertices_to_pairs (verts):
    """ convert list of vertices to pairs of vertical lines """
    ans = []
    for v1, v2 in zip(verts, verts[1:]):
        if v1[1] == v2[1]:
            a = min(v1[0], v2[0])
            b = max(v1[0], v2[0])
            ans.append([a, b, v1[1]]) # r1, r2, c1==c2 (r1 < r2)
    return ans

def find_next_pair (p, pairs):
    """ assume pairs are sorted """
    for i,q in enumerate(pairs):
        if pair_overlaps(p,q):
            return i,q
    return None, None

def merge_pairs (p1, p2):
    """ p2 is more on the right than p1 """
    r11 = p1[0]
    r12 = p1[1]
    r21 = p2[0]
    r22 = p2[1]
    c1 = p1[2]
    c2 = p2[2]
    assert(c2 >= c1)
    if r21 == r12:
        return [[r11,r22, c2]]
    if r11 == r22:
        return [[r21, r12, c2]]
    return [[r11,r21, c2], [r22,r12, c2]]

def merge_all_pairs (pairs):
    """ assume pairs are sorted """
    k = 0
    while True:
        k += 1
        print(f'{k=}')
        print(pairs)
        if len(pairs) == 2:
            break
        p = pairs[0]
        i,q = find_next_pair(p, pairs[1:])
        z = merge_pairs(p,q)
        new_pairs = pairs[1:][:i] + z + pairs[1:][i+1:] # insert z at i
        pairs = list(filter(lambda u:u[0] < u[1], new_pairs)) # remove flat edges
        print(pairs)

ins = read_instructions(sys.argv[1])

verts = instructions_to_vertices(ins)

print(f'{verts=}')

pairs = vertices_to_pairs (verts)
    
# sort pairs by incrasing cols
pairs = sorted(pairs, key=lambda u:u[2])

merge_all_pairs (pairs)