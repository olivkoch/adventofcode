import sys
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

mp = [c for line in lines for c in line]
mp = divide_chunks(mp, len(lines[0]))

rows = len(lines)
cols = len(lines[0])

# find start
start = [2,2]
for i, line in enumerate(lines):
    if 'S' in line:
        start[0] = i
        start[1] = line.index('S')
        break

# start has elevation a
mp[start[0]][start[1]] = 'a'

# find end
endg = [2,2]
for i, line in enumerate(lines):
    if 'E' in line:
        endg[0] = i
        endg[1] = line.index('E')
        break
mp[endg[0]][endg[1]] = 'z'
print(f'{endg=}')

def neighbors (p, rows, cols):
    ans = [[p[0]-1, p[1]], [p[0]+1, p[1]], [p[0], p[1]-1], [p[0], p[1]+1]]
    ans = filter(lambda u: u[0] >= 0 and u[1] >= 0 and u[0] < rows and u[1] < cols, ans)
    return list(ans)

def valid_move (mp, p, q):
    return ord(mp[q[0]][q[1]]) <= ord(mp[p[0]][p[1]]) + 1


sol = []
for sr in range(rows):
    for sc in range(cols):
        if mp[sr][sc] != 'a':
            continue
        start = [sr,sc]
        # shortest path from a to z
        visited = set()
        curr = copy.deepcopy(start)
        stopc = 'z'
        ans = 0
        queue = [(curr,0)]
        while queue:
            p, d = queue.pop(0)
            for r in neighbors(p, rows, cols):
                if valid_move(mp, p, r):
                    rt = tuple(r)
                    if not rt in visited:
                        queue.append((r, d+1))
                        visited.add(rt)
            if mp[p[0]][p[1]] == stopc:
                # print(f'stopping at {p} with depth {d} for target {stopc}')
                stop = [p[0], p[1]]
                ans += d
                break
        sol.append((ans, (sr, sc)))
sol = list(filter(lambda u:u[0]>0, sol))
print(min(sol, key=lambda u: u[0]))
