import sys
import re

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

ins = lines[0]

# read the map
mp = {}
for line in lines[2:]:
    # example: AAA = (BBB, BBB)
    m = re.match(r'^([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)$', line)
    if m is None:
        continue
    a = m.group(1)
    b = m.group(2)
    c = m.group(3)
    mp[a] = (b,c)

# execute instructions
i = 0
steps = 0
cur = 'AAA'
nins = len(ins)

while True:
    c = ins[i]
    i = (i+1) % nins
    steps += 1
    if c == 'L':
        cur = mp[cur][0]
    else:
        cur = mp[cur][1]
    if cur == 'ZZZ':
        break

print(steps)
