import re
import sys
import math

filename = sys.argv[1]

with open(filename,'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

print(lines)

x = [int(a) for a in re.findall(r'\d+', lines[0])] # race duration
y = [int(a) for a in re.findall(r'\d+', lines[1])] # record distance
z = zip(x,y)

# k = time spent pressing the button
# n = race duration
# y = record distance
# d = distance reached: k * (n - k)
# solve for d - y > 0
#
# - k^2 + k.n - y > 0
#
# discriminant = n^2 - 4y
# if disc. < 0 -> no solution
# if disc. == 0 -> one solution
# if disc. > 0 -> two solutions
#
# solution t = ( -n +/- sqrt(disc) ) / (-2)

def dist (d, x):
    """ d: duration, x: time pressed. Return distance traveled """
    return math.floor(x * (d-x))

def solve_race (d, r):
    """ d: duration, r: record.  Returns solutions """
    disc = d**2 - 4 * r
    if disc < 0:
        return None
    z1 = (-d - math.sqrt(disc)) / (-2)
    z2 = (-d + math.sqrt(disc)) / (-2)
    x1 = min([z1, z2])
    x2 = max([z1, z2])
    x1a = math.floor(x1)
    x1b = x1a + 1
    x1c = x1a - 1
    x2a = math.floor(x2)
    x2b = x2a + 1
    x2c = x2a - 1
    #print(f'--{x1a}, {x1b}, {x1c}')
    if dist(d, x1c) > r:
        print(f'{d}, {x1c}, {dist(d, x1c)} > {r}')
        x1 = x1c
    elif dist(d, x1a) > r:
        x1 = x1a
    elif dist(d, x1b) > r:
        x1 = x1b
    else:
        assert(False)
    if dist(d, x2b) > r:
        x2 = x2b
    elif dist(d, x2a) > r:
        x2 = x2a
    elif dist(d, x2c) > r:
        x2 = x2c
    else:
        assert(False)
    #print(f'{d}, {x1a},{r}, {dist(d, x1a)} {x1b}')
    return sorted((x1,x2))

ans = 1

for (d,r) in z:
    print(d,r)
    x = solve_race (d, r)
    if x is not None:
        ans *= (x[1] - x[0] + 1)
print(ans)
