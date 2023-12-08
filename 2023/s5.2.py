import sys
import re
import itertools
from collections import defaultdict

def convert_rev (u, ms):
    for m in ms:
        a, b, c = m
        if a <= u and u <= a + c - 1:
            return b + u - a
    return u

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

lineno = 0
mapno = 0
m = defaultdict(list)

# read converters

for line in lines:
    lineno += 1

    if lineno == 1:
        seeds = line.split(':')[1]
        seeds = re.findall(r'\d+', seeds)
        seeds = [int(x) for x in seeds]

    if line.find('map') != -1:
        mapno+=1
        continue

    d = [int(x) for x in re.findall(r'\d+', line)]

    if mapno > 0 and d:
        m[mapno].append(d)

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def is_in_seeds (u, seeds):
    for x in divide_chunks(seeds, 2):
        if x[0] <= u and u <= x[0] + x[1] -1:
            return True
    return False


# backward to seeds
ans = None
loc = None
#print(is_in_seeds (80, seeds))

for s in range(10000000):

    u = s

    for x in sorted(m.keys(), reverse=True):

        u = convert_rev(u, m[x])

    if is_in_seeds(u, seeds):
        ans = u
        loc = s
        break

print(f'seed = {ans}, location = {loc}')            
