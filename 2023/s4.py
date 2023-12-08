import sys
import re

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

ans = 0

for line in lines:
    
    c = 0
    seen = {}
    data = line.split(':')[1].split('|')
    xs = re.findall(r'(\d+)', data[0])
    ys = re.findall(r'(\d+)', data[1])
    for y in ys:
        if y in xs and not y in seen:
            c += 1
            seen[y] = 1
    if c == 1:
        ans += 1
    elif c > 1:
        ans += 2**(c-1)
print(ans)
