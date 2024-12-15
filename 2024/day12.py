import sys
import copy
from collections import defaultdict

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

rows = len(lines)
cols = len(lines[0])

X = [[lines[r][c] for c in range(rows)] for r in range(rows)]

V = [[False for _ in range(cols)] for _ in range(rows)]

def find_next(V, rows, cols):
    for r in range(rows):
        for c in range(cols):
            if not V[r][c]:
                return (r,c)
    return None

visited = set()

def neighbors(q, X, rows, cols):
    ans = [(q[0]-1, q[1]), (q[0]+1, q[1]), (q[0], q[1]-1), (q[0], q[1]+1)]
    ans = list(filter(lambda p: p[0] >= 0 and p[0] < rows and p[1] >=0 and p[1] < cols, ans))
    ans = list(filter(lambda p: X[p[0]][p[1]] ==  X[q[0]][q[1]], ans))
    return ans

# flood fills
areas = []
while True:
    if sum([len(x) for x in areas]) == rows * cols:
        break
    (r,c) = find_next(V, rows, cols)
    V[r][c] = True
    code = X[r][c]
    queue = [(r,c)]
    visited = set(queue)
    while queue:
        p = queue.pop()
        ns = neighbors(p, X, rows, cols)
        ns = list(filter(lambda a: not a in visited, ns))
        for q in ns:
            queue.append(q)
            visited.add(q)
            V[q[0]][q[1]] = True
    areas.append(copy.copy(visited))

def num_breaks(xs):
    """ return number of breaking points in a list """
    ans = 2
    prev = xs[0]
    for x in xs[1:]:
        if x > prev + 1:
            ans += 2
        prev = x
    return ans

def perimeter(pts):
    ans = 0
    byrow = defaultdict(list)
    for pt in pts:
        byrow[pt[0]].append(pt[1])
    for _, xs in byrow.items():
        xs = sorted(xs)
        ans += num_breaks(xs)
    bycols = defaultdict(list)
    for pt in pts:
        bycols[pt[1]].append(pt[0])
    for _, xs in bycols.items():
        xs = sorted(xs)
        ans += num_breaks(xs)
    return ans

def num_blocks(pts):
    """ return number of contiguous blocks in a 1D vector """
    if not pts:
        return 0
    x = pts[0]
    ans = 1
    for y in pts[1:]:
        if y > x + 1:
            ans += 1
        x = y
    return ans

def sides(pts):
    """ return number of sides for a zone """
    ans = 0
    byrow = defaultdict(list)
    for pt in pts:
        byrow[pt[0]].append(pt[1])
    past = set()
    for i in sorted(byrow.keys()):
        row = byrow[i]
        ys = set(row) - past
        ys = sorted(list(ys))
        # print(f'row {i}, {past}, {row}, {ys}, {num_blocks(ys)}')
        past = set(row)
        ans += num_blocks(ys)
    bycol = defaultdict(list)
    for pt in pts:
        bycol[pt[1]].append(pt[0])
    past = set()
    for i in sorted(bycol.keys()):
        col = bycol[i]
        ys = set(col) - past
        ys = sorted(list(ys))
        # print(f'col {i}, {past}, {row}, {ys}, {num_blocks(ys)}')
        past = set(col)
        ans += num_blocks(ys)
    return ans

def flip_points(pts, rows, cols):
    return [(rows-1-a[0],cols-1-a[1]) for a in pts]

perims = [perimeter(x) for x in areas]

surfaces = [len(a) for a in areas]

# part 1
out = sum([a*b for a,b in zip(surfaces, perims)])

# part 2
ssides = [sides(x) + sides(flip_points(x, rows, cols)) for x in areas]

out = sum([a*b for a,b in zip(surfaces, ssides)])

print(out)

