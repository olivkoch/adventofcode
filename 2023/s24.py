import sys
import re

filename = sys.argv[1]

lines = [a.strip() for a in open(filename, 'r').readlines()]

class Hail:

    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz

    def collide (self, other):
        return True
    

# main

for line in lines:
#    line = '1, 2, 3 @ 1, -2, 3'
#    line = '19, 13, 30 @ -2,  1, -2'
    x = re.match(r'(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)', line)
    x = [int(x.group(i)) for i in range(1,7)]
    h = Hail(x[0], x[1], x[2], x[3], x[4], x[5])
    print(x)
