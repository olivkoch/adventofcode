import sys

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

nr = len(lines)
nc = len(lines[0])
erow = '.' * nc

iss = []
for i,e in enumerate(lines):
    if e == erow:
        iss.append(i)

# duplicate empty lines in map
while True:
    if not iss:
        break
    i = iss.pop() # pop from the back
    lines[i:] = [erow] + lines[i:]
    nr += 1

# duplicate empty rows in map
iss = []
for c in range(nc):
    ise = True
    for r in range(nr):
        if lines[r][c] != '.':
            ise = False
            break
    if ise:
        iss.append(c)

print(nr,nc)

# duplicate empty cols
while True:
    if not iss:
        break
    i = iss.pop() # pop from the back
    for r in range(nr):
        lines[r] = lines[r][:i+1] + '.' + lines[r][i+1:]
    nc += 1

for line in lines:
    print(line)

# find galaxies
gal = []
for r in range(nr):
    for c in range(nc):
        if lines[r][c] == '#':
            gal.append((r,c))

dist = 0
for i in range(len(gal)):
    for j in range(i+1, len(gal)):
        g1 = gal[i]
        g2 = gal[j]
        dist += abs(g1[0]-g2[0]) + abs(g1[1]-g2[1]) 
print(dist)

