import sys
from collections import defaultdict
import copy

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

rows = len(lines)
cols = len(lines[0])

X = [[int(lines[r][c]) for c in range(cols)] for r in range(rows)]

# find zeros

zeros = [(r,c) for r in range(rows) for c in range(cols) if X[r][c] == 0]

def neighbors(X, s, rows, cols):
    ans = [(s[0] - 1, s[1]), (s[0] + 1, s[1]), (s[0], s[1] - 1), (s[0], s[1] + 1)]
    return list(filter(lambda u: u[0] >= 0 and u[0] < rows and u[1] >= 0 and u[1] < cols and X[u[0]][u[1]] == X[s[0]][s[1]] + 1, ans))

def find_paths (X, s, rows, cols):
    visited = set(s)
    paths = [[s]]
    done = False
    while not done:
        done = True
        for i, path in enumerate(paths):
            ns = neighbors(X, path[-1], rows, cols)
            ns = list(filter(lambda u: u not in visited, ns))
            if len(ns) == 1:
                y = ns[0]
                visited.add(y)
                path.append(y)
                done = False
            elif len(ns) > 1:
                paths.pop(i)
                for y in ns:
                    paths.append(path + [y])
                    visited.add(y)
                done = False
                break
    paths = list(filter(lambda p: X[p[-1][0]][p[-1][1]] == 9, paths))
    return paths

out = 0
for zero in zeros:
    ans = find_paths(X, zero, rows, cols)
    out += len(ans)
print(out)