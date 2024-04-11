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
            z[0] += s
        if d == 'L':
            z[0] -= s
        if d == 'U':
            z[1] -= s
        if d == 'D':
            z[1] += s
        ans.append(z)
    return ans[:-1], count

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

def test():
    p1 = [1903423, 1685151, -2211387]
    p2 = [1903423, 1945726, -2094186]
    p1, p2 = [2395024, 2717474, -4374143], [2395024, 2580641, -4045374]
    o = pair_overlaps(p1, p2)
    return o

def merge_pairs (p1, p2):
    """ p2 is more on the right than p1 """
    r11 = p1[0]
    r12 = p1[1]
    r21 = p2[0]
    r22 = p2[1]
    c1 = p1[2]
    c2 = p2[2]
    assert(c2 >= c1)
    s = (r12 - r11 + 1) * (c2 - c1) # surface of the square we're removing
    if r11 == r21 and r12 == r22:
        assert(r11 < r12)
        return None, s + (r12 - r11 + 1) # finishing a square 
    if r21 == r12:
        assert(r11 < r22)
        return [[r11,r22, c2]], s
    if r11 == r22:
        assert(r21 < r12)
        return [[r21, r12, c2]], s
    if r11 == r21:
        assert(r22 < r12)
        return [[r22, r12, c2]], s + r22 - r21 - 1
    if r12 == r22:
        assert(r11 < r21)
        return [[r11, r21, c2]], s + r22 - r21 - 1
    return [[r11,r21, c2], [r22,r12, c2]], s + r22 - r21 # splitting an edge

def sanity_check_pairs(pairs):
    for p in pairs:
        if p[0] > p[1]:
            return False
    return True

def sanity_check_pairs_advanced(pairs):
    for p1, p2 in zip(pairs, pairs[1:]):
        r11 = p1[0]
        r12 = p1[1]
        r21 = p2[0]
        r22 = p2[1]
        c1 = p1[2]
        c2 = p2[2]
        assert(c2 >= c1)
        if r11 == r22 or r12 == r21:
            return True
        if r11 == r21 and r12 == r22:
            return True
        if r11 == r21:
            return True
        if r12 == r22:
            return True
        if r21 > r11 and r22 < r12:
            return True
    return False
    
def merge_all_pairs (pairs):
    """ assume pairs are sorted """
    k = 0
    ans = 0
    while True:
        k += 1
        print(f'{k=}')
        #print(pairs)
        if len(pairs) == 2:
            break
        p = pairs[0]
        i,q = find_next_pair(p, pairs[1:])
        if not q:
            assert(False)
        print(f'merging {p} into {q}')
        z, s = merge_pairs(p,q)
        print(f'merged {p} into {q} --> {z}')
        ans += s
        if z:
            new_pairs = pairs[1:][:i] + z + pairs[1:][i+1:] # insert z at i
            pairs = new_pairs
        else:
            print(f'finished a square')
            new_pairs = pairs[1:][:i] + pairs[1:][i+1:] # skip pair i
            pairs = new_pairs
        assert(sanity_check_pairs(pairs))
        assert(sanity_check_pairs_advanced(pairs))
    print(f'last pairs: {pairs}')
    # last square
    p1 = pairs[0]
    p2 = pairs[1]
    ans += (p1[1] - p1[0] + 1) * (p2[2] - p1[2] + 1)
    return ans

ins = read_instructions(sys.argv[1])

verts, count = instructions_to_vertices(ins)

pairs = vertices_to_pairs (verts)
    
# sort pairs by incrasing cols
pairs = list(sorted(pairs, key=lambda u:u[2]))

assert(sanity_check_pairs(pairs))
assert(sanity_check_pairs_advanced(pairs))

#for i,p in enumerate(pairs):
    #if p[0] == 2319762:
#    print(i, p)
ans = merge_all_pairs (pairs)
#print(test())
#ans += count

print(ans)
print(952408144115 - ans)