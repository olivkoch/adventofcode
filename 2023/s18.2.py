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
    s = verts[0]
    for v1, v2 in zip(verts, verts[1:]):
        if v1[1] == v2[1]:
            a = min(v1[0], v2[0])
            b = max(v1[0], v2[0])
            ans.append([a, b, v1[1]]) # r1, r2, c1==c2 (r1 < r2)
    v1 = v2
    v2 = s
    a = min(v1[0], v2[0])
    b = max(v1[0], v2[0])
    ans.append([a, b, v1[1]])
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
    
def vertices_to_image(iverts, scale, filename):
    verts = [[int(x[0]/scale), int(x[1]/scale)] for x in iverts]
    rmin = min([p[0] for p in verts])
    rmax = max([p[0] for p in verts])
    cmin = min([p[1] for p in verts])
    cmax = max([p[1] for p in verts])
    irows = rmax - rmin + 1
    icols = cmax - cmin + 1
    arr = np.zeros((irows+1, icols+1), dtype=np.int32)
    count = 0
    for p1, p2 in zip(verts, verts[1:]):
        count += 1
        #if count > 7:
        #    break
        ir1 = p1[0] - rmin
        ic1 = p1[1] - cmin
        ir2 = p2[0] - rmin
        ic2 = p2[1] - cmin
        if ir1 == ir2:
            arr[ir1, ic1:ic2] = 255
            arr[ir1, ic2:ic1] = 255
        elif ic1 == ic2:
            arr[ir1:ir2, ic1] = 255
            arr[ir2:ir1, ic1] = 255
        else:
            print(p1, p2)
    im = Image.fromarray(arr).convert('RGB')
    im.save(filename)

def pairs_to_image(ipairs, scale, filename):
    pairs = [[int(u/scale) for u in p] for p in ipairs]
    rmin = min([p[0] for p in pairs] + [p[1] for p in pairs])
    rmax = max([p[0] for p in pairs] + [p[1] for p in pairs])
    cmin = min([p[2] for p in pairs])
    cmax = max([p[2] for p in pairs])
    irows = rmax - rmin + 1
    icols = cmax - cmin + 1
    arr = np.zeros((irows+1, icols+1), dtype=np.int32)
    for i,p1 in enumerate(pairs):
        for p2 in pairs[i+1:]:
            if pair_overlaps(p1, p2):
                ir11 = p1[0] - rmin
                ir12 = p1[1] - rmin
                ic1 = p1[2] - cmin
                ir21 = p2[0] - rmin
                ir22 = p2[1] - rmin
                ic2 = p2[2] - cmin
                assert(ir22 < irows)
                print(ic2, icols)
                assert(ic2 < icols)
                arr[ir11:ir12, ic1] = 255
                print(ir21, ir22, ic2, irows, icols)
                arr[ir21:ir22, ic2] = 255
                if ir11 == ir21 and ir12 == ir22:
                    arr[ir11, ic1:ic2] = 255
                    arr[ir12, ic1:ic2] = 255
                elif ir21 == ir12:
                    arr[ir21, ic1:ic2] = 255
                elif ir11 == ir22:
                    arr[ir11, ic1:ic2] = 255
                elif ir11 == ir21:
                    arr[ir11, ic1:ic2] = 255
                elif ir12 == ir22:
                    arr[ir12, ic1:ic2] = 255
                break
    im = Image.fromarray(arr).convert('RGB')
    im.save(filename)

    # for r,line in enumerate(mp):
    #     for c,u in enumerate(line):
    #         if u == '#':
    #             arr[r][c] = 255
    # im = Image.fromarray(arr).convert('RGB')
    # im = im.resize((int(cols*scale), int(rows*scale)), Image.Resampling.LANCZOS)
    # im.save(filename)


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

print(verts)

pairs = vertices_to_pairs (verts)

# sort pairs by incrasing cols
pairs = list(sorted(pairs, key=lambda u:u[2]))

print(pairs)

assert(sanity_check_pairs(pairs))
assert(sanity_check_pairs_advanced(pairs))

ans = merge_all_pairs (pairs)
print(ans)
print(952408144115 - ans)

#pairs_to_image(pairs, 1000, 'pairs.png')
#vertices_to_image(verts, 1000, 'verts.png')
