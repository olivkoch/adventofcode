import sys

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

nr = len(lines)
nc = len(lines[0])
erow = '.' * nc

isr = []

# list empty rows in map
for i,e in enumerate(lines):
    if e == erow:
        isr.append(i)

# list empty cols in map
isc = []
for c in range(nc):
    ise = True
    for r in range(nr):
        if lines[r][c] != '.':
            ise = False
            break
    if ise:
        isc.append(c)

# find galaxies
gal = []
for r in range(nr):
    for c in range(nc):
        if lines[r][c] == '#':
            gal.append((r,c))

def gal_dist(g1, g2, isr, isc):
    """ compute distance between two galaxies given empty rows and cols """
    ans = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
    minr = min([g1[0], g2[0]])
    maxr = max([g1[0], g2[0]])
    minc = min([g1[1], g2[1]])
    maxc = max([g1[1], g2[1]])
    for x in isr:
        if minr <= x and x <= maxr:
            ans += 1000000-1
    for y in isc:
        if minc <= y and y <= maxc:
            ans += 1000000-1
    return ans

# compute sum of distance pairs
dist = 0
for i in range(len(gal)):
    for j in range(i+1, len(gal)):
        g1 = gal[i]
        g2 = gal[j]
        dist += gal_dist(g1, g2, isr, isc)
print(dist)