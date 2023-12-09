import sys
import itertools

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

def compute(line):
    x = [[int(y) for y in line.split(' ')]]
    while sum([abs(c) for c in x[-1]]) > 0:
        x.append([b-a for (a,b) in itertools.pairwise(x[-1])])
    print(x)
    x[-1].append(0)
    print(x)
    for i in range(len(x)-2,-1,-1):
        w = x[i][-1] + x[i+1][-1]
        x[i].append(w)
    print(x)
    return x[0][-1]

ans = 0
for line in lines:
    ans += compute(line)
print(ans)