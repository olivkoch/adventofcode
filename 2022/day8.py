import sys

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

mp = [(int(a)) for line in lines for a in line]
mp = list(divide_chunks(mp, len(lines[0])))
rows = len(mp)
cols = len(mp[0])

ml = [[0 for _ in range(cols)] for _ in range(rows)]

# left
for r in range(1, rows-1):
    maxh = mp[r][0]
    for c in range(1, cols-1):
        if mp[r][c] > maxh:
            ml[r][c] = 1
        maxh = max(maxh, mp[r][c])

# right
for r in range(1, rows-1):
    maxh = mp[r][-1]
    for c in range(cols-2, 0, -1):
        if mp[r][c] > maxh:
            ml[r][c] = 1
        maxh = max(maxh, mp[r][c])

# top
for c in range(1, cols-1):
    maxh = mp[0][c]
    for r in range(1, rows-1):
        if mp[r][c] > maxh:
            ml[r][c] = 1
        maxh = max(maxh, mp[r][c])
    

# bottom
for c in range(1, cols-1):
    maxh = mp[-1][c]
    for r in range(rows-2, 0, -1):
        if mp[r][c] > maxh:
            ml[r][c] = 1
        maxh = max(maxh, mp[r][c])

out = sum([sum(a) for a in ml]) + 2 * rows + 2 *  (cols - 2)

def visibility (vec):
    """ compute left-ward visibility depth  """
    ans = []
    for i, x in enumerate(vec):
        hit = False
        for j in range(i-1, -1, -1):
            if vec[j] >= x:
                ans.append(i - j)
                hit = True
                break
        if not hit:
            ans.append(i)
    return ans

ml = [[0 for _ in range(cols)] for _ in range(rows)]
for r in range(rows):
    ml[r] = visibility(mp[r])    
    
mr = [[0 for _ in range(cols)] for _ in range(rows)]
for r in range(rows):
    mr[r] = visibility(mp[r][::-1])[::-1]

mu = [[0 for _ in range(cols)] for _ in range(rows)]
for c in range(cols):
    v = visibility([mp[i][c] for i in range(rows)])
    for i in range(rows):
        mu[i][c] = v[i]

md = [[0 for _ in range(cols)] for _ in range(rows)]
for c in range(cols):
    v = visibility([mp[i][c] for i in range(rows)][::-1])[::-1]
    for i in range(rows):
        md[i][c] = v[i]

mf = [[0 for _ in range(cols)] for _ in range(rows)]

for r in range(rows):
    for c in range(cols):
        mf[r][c] = ml[r][c] * mr[r][c] * mu[r][c] * md[r][c]

out = max([max(y) for y in mf])
print(out)