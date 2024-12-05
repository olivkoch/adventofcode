import sys
from collections import defaultdict

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

# read rules
rules = defaultdict(list)
for line in lines:
    if '|' in line:
        x = [int(a) for a in line.split('|')]
        rules[x[0]].append(x[1])

def swap (v, i, j):
    t = v[i]
    v[i] = v[j]
    v[j] = t

def fix_ordering(vec, rules):
    done = False
    while not done:
        done = True
        ud = {}
        for i, y in enumerate(vec):
            ud[y] = i
        for k, vs in rules.items():
            for v in vs:
                if k in ud and v in ud and ud[k] > ud[v]:
                    swap(vec, ud[k], ud[v])
                    done = False
                    break
            if not done:
                break

out = 0
for line in lines:
    if line and not '|' in line:
        x = [int(a) for a in line.split(',')]
        ud = {}
        for i, y in enumerate(x):
            ud[y] = i
        # check rules
        valid = True
        for k, vs in rules.items():
            for v in vs:
                if k in ud and v in ud and ud[k] > ud[v]:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            continue
        # fix line
        fix_ordering (x, rules)
        mid = x[int(len(x)/2)]
        out += mid

print(out)
