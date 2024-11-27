import sys

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

out = 0

def contains(x,y):
    return x[0] <= y[0] and y[1] <= x[1]

def overlaps(x,y):
    return contains(x,y) or (y[0] <= x[0] and x[0] <= y[1]) or (y[0] <= x[1] and x[1] <= y[1])

for line in lines:
    x = [int(a) for a in line.split(',')[0].split('-')]
    y = [int(a) for a in line.split(',')[1].split('-')]
    if overlaps(x,y) or overlaps(y,x):
        out += 1

print(out)