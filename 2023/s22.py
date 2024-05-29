import sys
from collections import defaultdict

filename = sys.argv[1]

data = [a.strip() for a in open(filename, 'r').readlines()]

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
    # sort bricks by min height
    bricks = sorted(bricks, key = lambda u: min(u[0][2], u[1][2]))
    for i in range(len(bricks)):
        b = bricks[i]
        s = b[0]
        e = b[1]
        # find the next blocking brick
        cds = [max(bricks[j][0][2], bricks[j][1][2]) for j in rmp[i]]
        h = max(cds) + 1 if cds else 1
        d = min(s[2], e[2])
        print (f'brick {i} {s=} {e=} will drop to height {h=} and has supports {rmp[i]}')
        assert (d >= h)
        dz = d - h
        bricks[i][0][2] -= dz
        bricks[i][1][2] -= dz


bricks = []
for line in data:
    a, b = read_bricks(line)
    bricks.append([a, b])

rmp = build_map (bricks)
print (rmp)

drop_bricks (bricks, rmp)