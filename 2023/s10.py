import sys
import copy

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

nr = len(lines)
nc = len(lines[0])

def find_start(lines):
    """ return the position of the S symbol """
    s = [x.find('S') for x in lines]
    x = [a > -1 for a in s]
    sr = x.index(True)
    sc = s[sr]
    return (sr,sc)

(sr,sc) = find_start(lines)
assert(lines[sr][sc]=='S')

def add_node (mp, a, b, c, d, nr, nc):
    if 0 <= a and a < nr and 0 <= b and b < nc:
        if 0 <= c and c < nr and 0 <= d and d < nc:
            mp[(a,b)].add((c,d))
            mp[(c,d)].add((a,b))
    return mp

def read_map(lines, nr, nc):
    """ return the map as a dict """
    ans = {}
    # empty map
    for r in range(nr):
        for c in range(nc):
            ans[(r,c)] = set()
    # read nodes
    for r,line in enumerate(lines):
        for c,x in enumerate(line):
            if x == '|':
                ans = add_node(ans,r ,c, r-1, c, nr, nc)
                ans = add_node(ans,r ,c, r+1, c, nr, nc)
            if x == '-':
                ans = add_node(ans,r ,c, r, c-1, nr, nc)
                ans = add_node(ans,r ,c, r, c+1, nr, nc)
            if x == 'L':
                ans = add_node(ans,r ,c, r-1, c, nr, nc)
                ans = add_node(ans,r ,c, r, c+1, nr, nc)
            if x == 'J':
                ans = add_node(ans,r ,c, r-1, c, nr, nc)
                ans = add_node(ans,r ,c, r, c-1, nr, nc)
            if x == '7':
                ans = add_node(ans,r ,c, r+1, c, nr, nc)
                ans = add_node(ans,r ,c, r, c-1, nr, nc)
            if x == 'F':
                ans = add_node(ans,r ,c, r+1, c, nr, nc)
                ans = add_node(ans,r ,c, r, c+1, nr, nc)
    return ans

graph = read_map(lines, nr, nc)
#print(graph)    

lines2 = [[x for x in line] for line in lines]
lines3 = [[x for x in line] for line in lines]


cur = list(graph[(sr,sc)])[0]
print(cur)
mv = 'right'
count = 0
lines2[sr][sc] = '!'
while True:
    lines3[cur[0]][cur[1]] = '*'
    type = lines[cur[0]][cur[1]]
    if type in ['|','L','J','S']:
        lines2[cur[0]][cur[1]] = '!'
    else:
        lines2[cur[0]][cur[1]] = '_'
    if type == 'J' and mv == 'right':
        mv = 'up'
        cur = (cur[0]-1,cur[1])
    if type == 'J' and mv == 'down':
        mv = 'left'
        cur = (cur[0],cur[1]-1)
    if type == '7' and mv == 'right':
        mv = 'down'
        cur = (cur[0]+1,cur[1])
    if type == '7' and mv == 'up':
        mv = 'left'
        cur = (cur[0],cur[1]-1)
    if type == '-' and mv == 'left':
        mv = 'left'
        cur = (cur[0],cur[1]-1)
    if type == '-' and mv == 'right':
        mv = 'right'
        cur = (cur[0],cur[1]+1)
    if type == '|' and mv == 'up':
        mv = 'up'
        cur = (cur[0]-1,cur[1])
    if type == '|' and mv == 'down':
        mv = 'down'
        cur = (cur[0]+1,cur[1])
    if type == 'F' and mv == 'up':
        mv = 'right'
        cur = (cur[0],cur[1]+1)
    if type == 'F' and mv == 'left':
        mv = 'down'
        cur = (cur[0]+1,cur[1])
    if type == 'L' and mv == 'left':
        mv = 'up'
        cur = (cur[0]-1,cur[1])
    if type == 'L' and mv == 'down':
        mv = 'right'
        cur = (cur[0],cur[1]+1)    
    if cur == (sr,sc):
        break
    count += 1

out = count/2+1
print(out)

for line in lines3:
    print(''.join(line))
print()

if True:
    ans = 0
    for u,line in enumerate(lines2):
        print(''.join(line))
        count = 0
        for v,c in enumerate(line):
            if c == '!':
                count += 1
                continue
            if count % 2 == 1 and c != '_' and c != 'S':
                ans += 1
                lines3[u][v]='#'
    print(ans)

print()
for line in lines3:
    print(''.join(line))
print()

print(ans)
