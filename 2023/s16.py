import sys
from collections import defaultdict

filename = sys.argv[1]

# read map
data = open(filename, 'r').readlines()

data = [line.strip().replace('\\','*') for line in data]

mp = [list(line) for line in data]

rows = len(mp)
cols = len(mp[0])

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def next_pos(pos, rows, cols):
    """ return the next position of the ray and a valid flag """
    r, c = pos[0], pos[1]
    dir = pos[2]
    if dir == UP:
        rn, cn = r-1, c
    if dir == RIGHT:
        rn, cn = r, c+1
    if dir == DOWN:
        rn, cn = r+1, c
    if dir == LEFT:
        rn, cn = r, c-1
    valid = (0 <= rn) and (rn < rows) and (0 <= cn) and (cn < cols)
    return [rn, cn, dir, valid]


rays = [[[0,0,RIGHT,True]]]
seen = set()
seen.add((0,0,RIGHT))
k = 0
while True:
    k += 1
    changed = False
    
    new_rays = []
    for i, ray in enumerate(rays): # action mirrors
        pos = ray[-1]
        r, c = pos[0], pos[1]
        x = mp[r][c]
        if not pos[3] or x == '.':
            continue
        if pos[2] == RIGHT and x == '/':
            rays[i][-1][2] = UP
        elif pos[2] == RIGHT and x == '*':
            rays[i][-1][2] = DOWN
        elif pos[2] == LEFT and x == '/':
            rays[i][-1][2] = DOWN
        elif pos[2] == LEFT and x == '*':
            rays[i][-1][2] = UP
        elif pos[2] == UP and x == '/':
            rays[i][-1][2] = RIGHT
        elif pos[2] == UP and x == '*':
            rays[i][-1][2] = LEFT
        elif pos[2] == DOWN and x == '/':
            rays[i][-1][2] = LEFT
        elif pos[2] == DOWN and x == '*':
            rays[i][-1][2] = RIGHT
        elif pos[2] in [RIGHT,LEFT] and x == '|':
            rays[i][-1][2] = UP
            new_rays.append([[r, c, DOWN, True]])
        elif pos[2] in [UP,DOWN] and x == '-':
            rays[i][-1][2] = LEFT
            new_rays.append([[r, c, RIGHT, True]])
    
    if new_rays:
        rays += new_rays
        changed = True

    for i, ray in enumerate(rays): # move each ray one step forward
        pos = ray[-1]
        if pos[3]: # only continue valid rays
            nxt = next_pos(pos, rows, cols)
            if nxt[-1]: # only continue if next position is valid
                head = tuple(nxt[:-1])
                if not head in seen: # don't track if we already passed here
                    rays[i].append(nxt)
                    seen.add(head)
                    changed = True
            else:
                rays[i][-1][3] = False

    if not changed:
        print(f'exiting at step {k}')
        break

print(rows, cols)
for line in data:
    print(line.strip())
print()

seen = set(map(lambda x:(x[0],x[1]), list(seen)))

out = [['.' for _ in range(cols)] for _ in range(rows)]
for s in seen:
    out[s[0]][s[1]] = '#'
for line in [''.join(x) for x in out]:
    print(line)

print(len(seen))
