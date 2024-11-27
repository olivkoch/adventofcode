import sys
import re

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

piles = [[] for _ in range(9)]

# read data
for k in range(7, -1, -1):
    print(lines[k])
    for r in range(9):
        if 4*r+1 < len(lines[k]):
            c = lines[k][4*r+1]
            if c != ' ':
                piles[r].append(c)

# read and execute orders
orders = lines[10:]
for od in orders:
    x = re.match(r'move (\d+) from (\d+) to (\d+)', od)
    num = int(x.groups()[0])
    src = int(x.groups()[1]) - 1
    tgt = int(x.groups()[2]) - 1
    q = len(piles[src])
    r = min(num, q)
    piles[tgt] += piles[src][-r:]
    piles[src] = piles[src][:-r]

out = ''.join([x[-1] for x in piles])
print(out)