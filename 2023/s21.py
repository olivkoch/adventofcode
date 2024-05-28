import sys

filename = sys.argv[1]

data = [a.strip() for a in open(filename, 'r').readlines()]

print(data)
rows = len(data)
cols = len(data[0])

# 0 = garden, 1 = rock, 2 = accessible
mp = [[0 for _ in range(cols)] for _ in range(rows)]

pos = None
for r in range(rows):
    for c in range(cols):
        mp[r][c] = 1 if data[r][c] == '#' else 0
        if data[r][c] == 'S':
            pos = [r,c]

mp[pos[0]][pos[1]] = 2

def neighbors (mp, rows, cols, r, c):
    ans = [(r-1,c), (r+1, c), (r, c-1), (r, c+1)]
    ans = filter(lambda u: u[0] >= 0 and u[1] >= 0 and u[0] < rows and u[1] < cols, ans)
    ans = filter(lambda u: mp[u[0]][u[1]] == 0, ans)
    return list(ans)

for _ in range(64):
    ans = []
    rem = []
    for r in range(rows):
        for c in range(cols):
            if mp[r][c] == 2:
                ans += neighbors(mp, rows, cols, r, c)
                rem.append((r,c))
    for u in rem:
        mp[u[0]][u[1]] = 0
    for u in ans:
        mp[u[0]][u[1]] = 2

ans = 0
for r in range(rows):
    for c in range(cols):
        if mp[r][c] == 2:
            ans += 1

print(ans, rows, cols)

