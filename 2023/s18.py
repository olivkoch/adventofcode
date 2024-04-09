import sys
import math
import numpy as np
from PIL import Image

def read_instructions(filename):
    filename = sys.argv[1]
    lines = open(filename, 'r').readlines()
    ins = [line.split(' ')[:2] for line in lines]
    return ins

def build_map(ins):
    curr = [0,0]
    min_r, max_r = math.inf, -math.inf
    min_c, max_c = math.inf, -math.inf
    pos = [curr]
    for i,n in enumerate(ins):
        d = n[0]
        s = int(n[1])
        if d == 'R':
            pos += [(curr[0], curr[1] + u) for u in range(s)]
            curr[1] += s
        if d == 'D':
            pos += [(curr[0] + u, curr[1]) for u in range(s)]
            curr[0] += s
        if d == 'U':
            pos += [(curr[0] - u, curr[1]) for u in range(s)]
            curr[0] -= s
        if d == 'L':
            pos += [(curr[0], curr[1] - u) for u in range(s)]
            curr[1] -= s
        min_r = min(min_r, curr[0])
        min_c = min(min_c, curr[1])
        max_r = max(max_r, curr[0])
        max_c = max(max_c, curr[1])
    rows = max_r - min_r + 1
    cols = max_c - min_c + 1
    out = [['.' for _ in range(cols)] for _ in range(rows)]
    print(rows, cols)
    for p in pos:
        try:
            out[p[0]-min_r][p[1]-min_c] = '#'
        except:
            print(p, min_r, min_c, rows, cols)
            assert(False)
    return out


def map_to_jpg(mp, filename, scale=2.0):
    rows, cols = len(mp), len(mp[0])
    arr = np.zeros((rows, cols), dtype=np.int32)
    for r,line in enumerate(mp):
        for c,u in enumerate(line):
            if u == '#':
                arr[r][c] = 255
    im = Image.fromarray(arr).convert('RGB')
    im = im.resize((int(cols*scale), int(rows*scale)), Image.Resampling.LANCZOS)
    im.save(filename)

def find_interior_point(mp):
    for r,line in enumerate(mp):
        x = 0
        for c,u in enumerate(line):
            if u == '#':
                x = 1
            if u == '.' and x == 1:
                if '#' in line[c+1:]:
                    return (r,c)
    return None

def neighbors(p, rows, cols):
    out = [(p[0]-1, p[1]), (p[0]+1, p[1]), (p[0], p[1]-1), (p[0], p[1]+1)]
    out = filter(lambda x:x[0] >= 0, out)
    out = filter(lambda x:x[1] >= 0, out)
    out = filter(lambda x:x[0] < rows, out)
    out = filter(lambda x:x[1] < cols, out)
    return list(out)
    
def print_map(mp):
    print()
    for line in mp:
        print (''.join(line))
    print()

def flood_fill(mp, p, rows, cols):
    r, c = p[0], p[1]
    assert(mp[r][c] == '.')
    targets = [(r,c)]
    count = 0
    while True:
        nt = len(targets)
        for t in targets:
            ns = neighbors(t, rows, cols)
            for n in ns:
                if mp[n[0]][n[1]] == '.':
                    mp[n[0]][n[1]] = '#'
                    targets += [n]
                    count += 1
        targets = targets[nt:]
        if not targets:
            break
    return count

ins = read_instructions(sys.argv[1])

mp = build_map(ins)

print_map(mp)

map_to_jpg(mp, 'mp.jpg')

rows, cols = len(mp), len(mp[0])

ans = sum([x == '#' for line in mp for x in line])
while True:
    p = find_interior_point(mp)
    print(f'new interior point {p}')
    if not p:
        break
    ans += flood_fill(mp, p, rows, cols)
    print_map(mp)

print(ans)
