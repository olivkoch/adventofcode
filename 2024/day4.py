import sys
import re
import copy

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

def divide_chunks(l, n):
    # looping till length l
    ans = []
    for i in range(0, len(l), n): 
        ans.append(l[i:i + n])
    return ans

def transpose (lines):
    rows = len(lines)
    cols = len(lines[0])
    x = divide_chunks([c for line in lines for c in line], rows)
    xt = [[x[r][c] for r in range(rows)] for c in range(cols)]
    ans = [''.join(u) for u in xt]
    return ans

def flip_vertical(lines):
    rows = len(lines)
    cols = len(lines[0])
    x = divide_chunks([c for line in lines for c in line], rows)
    xt = [[x[r][cols-1-c] for c in range(cols)] for r in range(rows)]
    ans = [''.join(u) for u in xt]
    return ans

def in_bounds (p, rows, cols):
    return p[0] >= 0 and p[0] < rows and p[1] >= 0 and p[1] < cols

def diagonal(lines):
    rows = len(lines)
    cols = len(lines[0])
    x = divide_chunks([c for line in lines for c in line], rows)
    d = [-1,1]
    curr = [0,0]
    count = 0
    ans = []
    while count < rows * cols:
        y = []
        while in_bounds (curr, rows, cols):
            y.append(x[curr[0]][curr[1]])
            curr[0] += d[0]
            curr[1] += d[1]
        # step back
        curr[0] -= d[0]
        curr[1] -= d[1]
        # next stride
        if d[0] == -1:
            curr[1] += 1
            if curr[1] == cols:
                curr[1] -= 1
                curr[0] += 1
        else:
            curr[0] += 1
            if curr[0] == rows:
                curr[0] -= 1
                curr[1] += 1
        # flip direction
        d[0] *= -1
        d[1] *= -1
        count += len(y)
        ans.append(''.join(y))
    return ans

def count_instances (lines):
    out = 0
    for line in lines:
        a = re.findall(r'XMAS', line)
        if a:
            out += len(a)
        a = re.findall(r'SAMX', line)
        if a:
            out += len(a)
    return out

def is_crossing (x, r, c):
    u = ''.join([x[r-1][c-1], x[r][c], x[r+1][c+1]])
    v = ''.join([x[r-1][c+1], x[r][c], x[r+1][c-1]])
    return u in ['MAS', 'SAM'] and v in ['MAS', 'SAM']

def find_crossings(lines):
    out = 0
    rows = len(lines)
    cols = len(lines[0])
    x = divide_chunks([c for line in lines for c in line], rows)
    for r in range(1, rows-1):
        for c in range(1, cols-1):
            if is_crossing(x, r, c):
                out += 1
    return out

ans = 0

ans += count_instances(lines)

# transpose
y = transpose(lines)
ans += count_instances(y)

# diagonal
y = diagonal(lines)
ans += count_instances(y)

# diagonal
y = diagonal(flip_vertical(lines))
ans += count_instances(y)

print(ans)

# part two
ans = find_crossings(lines)
print(ans)
