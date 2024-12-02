import sys
from collections import defaultdict

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

def list_lists (vec):
    n = len(vec)
    for k in range(n-1):
        yield vec[:k] + vec[k+1:]
    yield vec[:n-1]

out = 0
for line in lines:
    if not line:
        break
    xxs = [int(a) for a in line.split(' ')]
    for xs in list_lists(xxs):
        if sorted(xs) == xs or sorted(xs, reverse=True) == xs:
            valid = True
            for x1, x2 in zip(xs, xs[1:]):
                if abs(x2-x1) > 3 or abs(x2-x1) == 0:
                    valid = False
                    break
            if valid:
                print(xxs)
                out += 1
                break

print(out)