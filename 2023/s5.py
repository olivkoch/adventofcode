import sys
import re
from collections import defaultdict

def convert (u, ms):
    for m in ms:
        a, b, c = m
        if b <= u and u <= b + c - 1:
            return a + u - b
    return u

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

lineno = 0
mapno = 0
m = defaultdict(list)

# read converters

for line in lines:
    lineno += 1

    if lineno == 1:
        seeds = line.split(':')[1]
        seeds = re.findall(r'\d+', seeds)
        seeds = [int(x) for x in seeds]

    if line.find('map') != -1:
        mapno+=1
        continue

    d = [int(x) for x in re.findall(r'\d+', line)]

    if mapno > 0 and d:
        m[mapno].append(d)

# compute seed locations
locs = []

for seed in seeds:

    u = seed

    for x in sorted(m.keys()):
    
        u = convert (u, m[x])

    locs.append(u)

print(min(locs))

