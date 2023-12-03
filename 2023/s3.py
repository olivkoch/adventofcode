import re
import sys

# replace '-' chars by another symbol
filename = sys.argv[1]
with open(filename,'r') as fh:
    lines = [s.strip().replace('-','*') for s in fh.readlines()]

    
print(lines)
num_lines = len(lines)
width = len(lines[0])

# find all numbers
n_locs = []
for i,line in enumerate(lines):
    for m in re.finditer(r'\d+', line):
        u = m.start(0)
        v = m.end(0)-1
        n_locs.append((i,u,v))

# find all symbols
s_locs = []
for i,line in enumerate(lines):
    for m in re.finditer(r'[^\d\.-]', line):
        u = m.start(0)
        s_locs.append((i,u))

def is_adjacent(r, c1, c2, u, v):
    if r-1 <= u and u <= r+1:
        if c1-1 <= v and v <= c2+1:
            return True
    return False

ans = 0
for n_loc in n_locs:
    keep = False
    r = n_loc[0]
    c1 = n_loc[1]
    c2 = n_loc[2]
    for s_loc in s_locs:
        if is_adjacent(r, c1, c2, s_loc[0], s_loc[1]):
            keep = True
            break
    if keep:
        t = int(lines[r][c1:c2+1])
        print(f'keeping {t} at row {r}')
        ans += int(lines[r][c1:c2+1])

print(ans)

