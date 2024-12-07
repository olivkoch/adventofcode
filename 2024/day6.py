import sys
from collections import defaultdict

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

# read map
rows = len(lines)
cols = len(lines[0])
P = [[0 for _ in range(cols)] for _ in range(rows)]
for r, line in enumerate(lines):
    for c, x in enumerate(line):
        P[r][c] = 1 if x == '#' else 0

# find position
dir2xy = {0: (0,1), 1:(1,0), 2:(0,-1), 3:(-1,0)}

def starting_point (lines):
    for r, line in enumerate(lines):
        for c, x in enumerate(line):
            if x == '>':
                dir = 0
                curr = [r,c]
            elif x == 'V':
                dir = 1
                curr = [r,c]
            elif x == '<':
                dir = 2
                curr = [r,c]
            elif x == '^':
                dir = 3
                curr = [r,c]
    return curr, dir

def in_bounds(p, rows, cols):
    return p[0] >= 0 and p[0] < rows and p[1] >= 0 and p[1] < cols

assert(dir is not None)

# curr, dir = starting_point (lines)
# visited = set()
# while in_bounds(curr, rows, cols):
#     visited.add(tuple(curr))
#     f = dir2xy[dir]
#     nxt = [curr[0] + f[0], curr[1] + f[1]]
#     if in_bounds(nxt, rows, cols) and P[nxt[0]][nxt[1]] == 1:
#         dir = (dir + 1) % 4
#     else:
#         curr[0] = nxt[0]
#         curr[1] = nxt[1]

# ans = len(visited)
# print(ans)

# part 2
ans = 0
for r in range(rows):
    for c in range(cols):
        if P[r][c] != 0:
            continue

        P[r][c] = 1

        visited = defaultdict(list)
        stuck = False
        
        curr, dir = starting_point(lines)

        while in_bounds(curr, rows, cols):
            if dir in visited[tuple(curr)]:
                stuck = True
                break 
            visited[tuple(curr)].append(dir)
            f = dir2xy[dir]
            nxt = [curr[0] + f[0], curr[1] + f[1]]
            if in_bounds(nxt, rows, cols) and P[nxt[0]][nxt[1]] == 1:
                dir = (dir + 1) % 4
            else:
                curr[0] = nxt[0]
                curr[1] = nxt[1]
        if stuck:
            ans += 1

        P[r][c] = 0

print(ans)





        



