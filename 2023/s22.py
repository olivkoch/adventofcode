import sys
from collections import defaultdict
from PIL import Image
import numpy as np
import random

filename = sys.argv[1]

data = [a.strip() for a in open(filename, 'r').readlines()]

def map_to_jpg(mp, filename, scale=1.0):
    rows, cols = len(mp), len(mp[0])
    arr = np.zeros((rows, cols), dtype=np.int32)
    im = Image.fromarray(arr).convert('RGB')
    pixels = im.load()
    codesr = list(range(18000))
    codesg = list(range(18000))
    codesb = list(range(18000))
    random.shuffle(codesr)
    random.shuffle(codesg)
    random.shuffle(codesb)
    for r,line in enumerate(mp):
        for c,u in enumerate(line):
            if u > 0:
                pixels[c,r] = ((49 * codesr[u]) % 255, (53 * codesg[u]) % 255, (27 * codesb[u]) % 255)
    im = im.resize((int(cols*scale), int(rows*scale)), Image.Resampling.LANCZOS)
    im.save(filename)

def read_bricks(line):
    x = line.split('~')
    a = [int(u) for u in x[0].split(',')]
    b = [int(u) for u in x[1].split(',')]
    return a, b

def build_map (bricks):
    mp = defaultdict(list) # map (x,y) to a list of brick ids sorted by height
    for i, b in enumerate(bricks):
        s = b[0]
        e = b[1]
        for u in range(s[0], e[0]+1):
            for v in range(s[1], e[1]+1):
                for w in range(s[2], e[2]+1):
                    mp[(u,v)].append ((w, i))
    rmp = defaultdict(set) # map a brick id to all brick ids that sit under it
    for k, v in mp.items():
        z = sorted(v, key = lambda u:u[0], reverse=True)
        for i, a in enumerate(z):
            for b in z[i+1:]:
                if b[1] != a[1]:
                    rmp[a[1]].add(b[1])
    return rmp

        
def drop_bricks (bricks, rmp):
    """ rmp maps a brick id to all brick ids that sit under it """
    for i in range(len(bricks)):
        b = bricks[i]
        s = b[0]
        e = b[1]
        # find the next blocking brick
        cds = [max(bricks[j][0][2], bricks[j][1][2]) for j in rmp[i]]
        h = max(cds) + 1 if cds else 1
        d = min(s[2], e[2])
        # print (f'brick {i} {s=} {e=} will drop to height {h=} and has supports {rmp[i]}')
        assert (d >= h)
        dz = d - h
        bricks[i][0][2] -= dz
        bricks[i][1][2] -= dz

def bricks_can_destroy(bricks, rmp):
    """ rmp maps a brick id to all brick ids that sit under it """
    ans = set()
    for k, v in rmp.items():
        bk = bricks[k]
        bkh = min(bk[0][2], bk[1][2])
        bv = list(filter (lambda u: max(bricks[u][0][2], bricks[u][1][2]) == bkh - 1, v))
        if len(bv) == 1:
            # Brick {k} sits on just brick {bv[0]}
            ans.add(bv[0])
    return ans, len(bricks) - len(ans)

def get_weight (mp, xmp, i):
    """ <mp> maps a brick id to bricks sitting directly on top of it 
        <xmp> maps a brick id to bricks sitting directly under it 
        <i> is the brick id """
    visited = set()
    queue = [i]
    while (queue):
        cur = queue.pop(0)
        if not cur in visited:
            visited.add(cur)
        queue += list(mp[cur])
    count = 0
    # would these bricks actually fall?
    for v in visited:
        if v == i:
            count += 1
            continue
        k = 0
        for w in xmp[v]:
            if w in visited:
                k += 1
        if k == len(xmp[v]):
            count += 1
        #else:
        #    print (f'{v} would not fall for {i}!')
    return count - 1

def build_graph (bricks, rmp):
    """ maps a brick id to bricks sitting directly on top of / under it
        <rmp> maps a brick id to all brick ids that sit under it """
    mp = defaultdict(set)
    xmp = defaultdict(set)
    for k, v in rmp.items():
        bk = bricks[k]
        bkh = min(bk[0][2], bk[1][2])
        for u in v:
            bu = bricks[u]
            buh = max(bu[0][2], bu[1][2])
            if bkh == buh + 1:
                mp[u].add(k)
                xmp[k].add(u)
                # print(f'{k} sits directly on top of {u}')
    return mp, xmp

def bricks_to_map (bricks):
    maxx = max([max(b[0][0], b[1][0]) for b in bricks])
    maxy = max([max(b[0][1], b[1][1]) for b in bricks])
    maxz = max([max(b[0][2], b[1][2]) for b in bricks])
    ans = [[0 for _ in range (maxx + 1)] for _ in range(maxz + 1)]
    print(f'dim = {maxx}, {maxz}')
    for i, b in enumerate(bricks):
        for x in range(b[0][0], b[1][0]+1):
            for z in range(b[0][2], b[1][2]+1):
                ans[z][x] = i + 1
    return ans

# read bricks
bricks = []
for line in data:
    a, b = read_bricks(line)
    bricks.append([a, b])

# sort bricks by min height
    bricks = sorted(bricks, key = lambda u: min(u[0][2], u[1][2]))

rmp = build_map (bricks)

drop_bricks (bricks, rmp)

bs, _ = bricks_can_destroy (bricks, rmp)

mp, xmp = build_graph (bricks, rmp)

ans = 0
for b in bs:
    ans += get_weight(mp, xmp, b)
print(ans)

#ans = sum([get_weight(mp, k) for k in bs])
#print(ans)

# mp = bricks_to_map (bricks)

# map_to_jpg (mp, f'day-22.png', scale=1)