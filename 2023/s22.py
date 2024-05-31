import sys
from collections import defaultdict
from PIL import Image
import numpy as np
import random

# colors for display
random.seed(123)
codesr = list(range(18000))
codesg = list(range(18000))
codesb = list(range(18000))
random.shuffle(codesr)
random.shuffle(codesg)
random.shuffle(codesb)

filename = sys.argv[1]

data = [a.strip() for a in open(filename, 'r').readlines()]

def map_to_img(mp, scale=1.0):
    rows, cols = len(mp), len(mp[0])
    arr = np.zeros((rows, cols), dtype=np.int32)
    im = Image.fromarray(arr).convert('RGB')
    pixels = im.load()
    h = im.size[1]
    for r,line in enumerate(mp):
        for c,u in enumerate(line):
            if u > 0:
                pixels[c,h-r] = ((49 * codesr[u]) % 255, (53 * codesg[u]) % 255, (27 * codesb[u]) % 255)
    im = im.resize((int(cols*scale), int(rows*scale)), Image.Resampling.LANCZOS)
    return im

def save_images (im1, im2, filename):
    assert(im1.size[1] == im2.size[1])
    rows = im1.size[1]
    ofs = 3
    cols = im1.size[0] + im2.size[0] + ofs
    arr = np.zeros((rows, cols), dtype=np.int32)
    im = Image.fromarray(arr).convert('RGB')
    pix = im.load()
    pix1 = im1.load()
    pix2 = im2.load()
    for r in range(rows):
        for c in range(im1.size[0]):
            pix[c,r] = pix1[c,r]
    for r in range(rows):
        for c in range(im2.size[0]):
            pix[c + im1.size[0] + ofs,r] = pix2[c,r]
    im.save(filename)

def read_bricks(line):
    x = line.split('~')
    a = [int(u) for u in x[0].split(',')]
    b = [int(u) for u in x[1].split(',')]
    return a, b

def build_map (bricks):
    """ map a brick id to all brick ids that sit under it """
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
    """ drop all bricks, assuming bricks are sorting by increasing min height
        <rmp> maps a brick id to all brick ids that sit under it """
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

def list_brick_xy (bricks, i):
    """ list positions of the brick on the x,y plane """
    a = set()
    s = bricks[i][0]
    e = bricks[i][1]
    for u in range(s[0], e[0]+1):
        for v in range(s[1], e[1]+1):
            a.add((u,v))
    return a

def bricks_overlap_xy (bricks, i, j):
    """ return true if bricks i and j overlap on the horizontal plane """
    a = list_brick_xy (bricks, i)
    b = list_brick_xy (bricks, j)
    return len(a.intersection(b)) > 0

def bricks_can_destroy(bricks, rmp):
    """ return number of bricks that can be safely destroyed
        <rmp> maps a brick id to all brick ids that sit under it """
    ans = set()
    for k, v in rmp.items():
        bk = bricks[k]
        bkh = min(bk[0][2], bk[1][2])
        bv = list(filter (lambda u: max(bricks[u][0][2], bricks[u][1][2]) == bkh - 1, v))
        if len(bv) == 1:
            # Brick k sits only on brick bv[0] so we can't destroy bv[0]
            ans.add(bv[0])
    return ans, len(bricks) - len(ans)

def falls (i, xmp, dropped):
    """ return true if brick i falls given all bricks that dropped already 
        <xmp> maps a brick id to bricks sitting directly under it 
    """
    return len (xmp[i] - dropped) == 0

def get_weight (mp, xmp, i):
    """ return the number of bricks that fall if i falls (chain reaction)
        <mp> maps a brick id to bricks sitting directly on top of it 
        <xmp> maps a brick id to bricks sitting directly under it 
    """
    queue = [{i}]
    dropped = {i}
    while (queue):
        cs = queue.pop(0)
        cands = [u for c in cs for u in mp[c]] # all new bricks that could fall
        new_dropped = set()
        for cand in cands:
            if falls (cand, xmp, dropped):
                new_dropped.add(cand)
        if new_dropped:
            queue.append(new_dropped)
            dropped = dropped.union(new_dropped)
    return len(dropped) - 1

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
                # k sits directly on top of u
                mp[u].add(k)
                xmp[k].add(u)
    return mp, xmp

def bricks_to_maps (bricks):
    maxx = max([max(b[0][0], b[1][0]) for b in bricks])
    maxy = max([max(b[0][1], b[1][1]) for b in bricks])
    maxz = max([max(b[0][2], b[1][2]) for b in bricks])
    ansx = [[0 for _ in range (maxx + 1)] for _ in range(maxz + 1)]
    print(f'dim = {maxx}, {maxz}')
    for i, b in enumerate(bricks):
        for x in range(b[0][0], b[1][0]+1):
            for z in range(b[0][2], b[1][2]+1):
                ansx[z][x] = i + 1
    ansy = [[0 for _ in range (maxy + 1)] for _ in range(maxz + 1)]
    for i, b in enumerate(bricks):
        for y in range(b[0][1], b[1][1]+1):
            for z in range(b[0][2], b[1][2]+1):
                ansy[z][y] = i + 1    
    return ansx, ansy

def check_bricks (bricks):
    """ check that all bricks have been dropped
        i.e. no brick should have only void under it
    """
    maxx = max([max(b[0][0], b[1][0]) for b in bricks])
    maxy = max([max(b[0][1], b[1][1]) for b in bricks])
    maxz = max([max(b[0][2], b[1][2]) for b in bricks])
    m = np.zeros((maxx + 1, maxy + 1, maxz + 1), dtype=np.int32)-1
    for i, b in enumerate(bricks):
        for x in range(b[0][0], b[1][0]+1):
            for y in range(b[0][1], b[1][1]+1):
                for z in range(b[0][2], b[1][2]+1):
                    m[x, y, z] = i
    for i, b in enumerate(bricks):
        at_bottom = False
        is_supported = False
        for x in range(b[0][0], b[1][0]+1):
            for y in range(b[0][1], b[1][1]+1):
                for z in range(b[0][2], b[1][2]+1):
                    assert (m[x, y, z] == i)
                    if z == 1:
                        at_bottom = True
                        break
                    if m[x, y, z - 1] != -1 and m[x, y, z - 1] != m[x, y, z]:
                        is_supported = True
                        break
        if not (at_bottom or is_supported):
            print (f'Oups.  Brick {i} is in the air {bricks[i]}')



# read bricks
bricks = []
for line in data:
    a, b = read_bricks(line)
    bricks.append([a, b])

# sort bricks by min height
bricks = sorted(bricks, key = lambda u: min(u[0][2], u[1][2]))

rmp = build_map (bricks)

drop_bricks (bricks, rmp)

bs, ans = bricks_can_destroy (bricks, rmp)

print (f'can be destroyed {ans}')

mp, xmp = build_graph (bricks, rmp)

ans = 0
for b in bs:
    ans += get_weight(mp, xmp, b)
print(ans)

mp_x, mp_y = bricks_to_maps (bricks)

im_x = map_to_img (mp_x, scale=1)
im_y = map_to_img (mp_y, scale=1)

save_images(im_x, im_y, f'day-22-{len(bricks)}.png')

check_bricks (bricks)
