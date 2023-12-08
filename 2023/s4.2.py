import sys
import re

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

ans = 0

lineno = 0
wins = {}
losers = []

for line in lines:
    lineno += 1
    data = line.split(':')[1].split('|')
    xs = re.findall(r'(\d+)', data[0])
    ys = re.findall(r'(\d+)', data[1])
    score = 0
    for y in ys:
        if y in xs:
            score += 1
    if score > 0:
        wins[lineno] = score
    else:
        losers.append(lineno)

nl = len(lines)

ks = sorted(wins.keys())
ids = [k for k in ks]

for k in ks:
 #   print(k)
    adds = []
    for d in ids:
        if d == k:
            adds += list(range(k+1, min([nl+1, k+1+wins[k]])))
#    print(adds)
    if len(adds) == 0:
        break
    ids += adds
    print(len(ids))
#    print(f'ids = {ids}')
ids += losers
#print(sorted(ids))
print(len(ids))
