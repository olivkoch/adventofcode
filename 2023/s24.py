import sys
import re
import numpy as np

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
        self.d = x * dy - y * dx

    def __str__ (self):
        return f'({self.x}, {self.y}, {self.z}, {self.dx}, {self.dy}, {self.dz})'
    
    def collide (self, other, rmin, rmax, debug=False):
        A = np.array([[self.dy, -self.dx], [other.dy, -other.dx]])
        det = np.linalg.det(A)
        if abs(det) < 1e-6:
            return False
        Ainv = np.linalg.inv(A)
        B = np.array([[self.d], [other.d]])
        X = np.matmul(Ainv, B)
        t1 = (X[0] - self.x) / self.dx
        t2 = (X[0] - other.x) / other.dx
        return t1[0] >= 0 and t2[0] >= 0 and rmin < X[0] and X[0] < rmax and rmin < X[1] and X[1] < rmax
    

# main
xmin = 200000000000000
xmax = 400000000000000

hails = []
for line in lines:
    x = re.match(r'(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)', line)
    x = [int(x.group(i)) for i in range(1,7)]
    h = Hail(x[0], x[1], x[2], x[3], x[4], x[5])
    hails.append(h)

# unit test
# h1 = Hail(19, 13, 30, -2, 1, -2)
# h2 = Hail(12, 31, 28, -1, -2, -1)
# ans = h1.collide(h2, xmin, xmax)
# print(ans)


count = 0
for i, h1 in enumerate(hails):
    for h2 in hails[i+1:]:
        if h1.collide(h2, xmin, xmax):
            count += 1

print(count)

