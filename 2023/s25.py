import sys
import random
from collections import defaultdict

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

g = defaultdict(set)

for line in lines:
    a = line.split(':')
    h = a[0]
    xs = [a.strip() for a in a[1].strip().split(' ')]
    for x in xs:
        g[h].add(x)
        g[x].add(h)

def dijkstra (g, src, tgt):
    """ find shortest path between src and tgt """
    visited = set()
    q = [src]
    visited.add(src)
    prev = {}
    prev[src] = None
    while q:
        x = q.pop(0)
        for y in g[x]:
            if not y in visited:
                visited.add(y)
                q.append(y)
                prev[y] = x
        if x == tgt:
            break
    if tgt in prev:
        path = [tgt]
        while path[-1] != src:
            path.append(prev[path[-1]])
        return path
    return None

def graph_size (g, src):
    visited = set()
    visited.add(src)
    q = [src]
    while (q):
        x = q.pop(0)
        for y in g[x]:
            if not y in visited:
                visited.add(y)
                q.append(y)
    return len(visited)


nodes = list(g.keys())
pairs = defaultdict(int)

for _ in range(10000):
    src = random.choice(nodes)
    tgt = random.choice(nodes)
    if src == tgt:
        continue
    path = dijkstra(g, src, tgt)
    for p1, p2 in zip(path, path[1:]):
        pairs[(min(p1, p2), max(p1, p2))] += 1

qs = sorted ([(k,v) for k, v in pairs.items()], key=lambda u: u[1], reverse=True)

for q in qs[:3]:
    # remove the top 3 edges
    a = q[0][0]
    b = q[0][1]
    g[a].remove(b)
    g[b].remove(a)

ss = set()
for i in range(len(nodes)):
    ss.add(graph_size(g, nodes[i]))
    if len(ss) == 2:
        break
print(ss)