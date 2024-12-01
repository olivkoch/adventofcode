import sys
from collections import defaultdict

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

x = [int(a.split('  ')[0]) for a in lines]
y = [int(a.split('  ')[1]) for a in lines]

a = x#sorted(list(set(x)))
b = defaultdict(int)
for u in y:
    b[u] += 1

out = 0

for u in a:
    out += u * b[u]

print(out)