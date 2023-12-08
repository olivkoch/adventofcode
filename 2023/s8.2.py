import sys
import re
import math

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

ins = lines[0]

# read the map
mp = {}
for line in lines[2:]:
    # example: AAA = (BBB, BBB)
    m = re.match(r'^([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)$', line)
    if m is None:
        continue
    a = m.group(1)
    b = m.group(2)
    c = m.group(3)
    mp[a] = (b,c)

# find start nodes
nodes = list(filter(lambda x : x[-1] == 'A', mp.keys()))

nins = len(ins)

# find number of steps to Zs for each lane
lanes = []
for node in nodes:
    ans = []
    cur = node
    i = 0
    steps = 0
    while True:
        c = ins[i]
        i = (i+1) % nins
        steps += 1
        if c == 'L':
            cur = mp[cur][0]
        else:
            cur = mp[cur][1]
        if cur[-1] == 'Z':
            lanes.append(steps)
            break
        
print(lanes)
ans = math.lcm(*lanes)
print(ans)