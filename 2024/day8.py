import sys
from collections import defaultdict

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

rows = len(lines)
cols = len(lines[0])

freqs = set([c for line in lines for c in line]) - set('.')
Q = defaultdict(list)

for r, line in enumerate(lines):
    for c, x in enumerate(line):
        if x != '.':
            Q[x].append((r,c))

def antinodes(v1, v2, rows, cols):
    dr = v2[0] - v1[0]
    dc = v2[1] - v1[1]
    ans = [v1, v2]
    k = 1
    while True:
        x = (v1[0] + k*dr, v1[1] + k*dc)
        if not in_bound(x, rows, cols):
            break
        ans.append(x)
        k += 1
    k = -1
    while True:
        x = (v1[0] + k*dr, v1[1] + k*dc)
        if not in_bound(x, rows, cols):
            break
        ans.append(x)
        k -= 1
    return set(ans)

def in_bound(v, rows, cols):
    return v[0] >= 0 and v[0] < rows and v[1] >= 0 and v[1] < cols

nodes = set()

for f, vs in Q.items():
    for i, v1 in enumerate(vs):
        for j, v2 in enumerate(vs[i+1:]):
            xs = antinodes(v1, v2, rows, cols)
            nodes = nodes | xs

print(len(nodes))
