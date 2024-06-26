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
        self.p = np.array([x, y, z])
        self.v = np.array([dx, dy, dz])

    def __str__ (self):
        return f'({self.x}, {self.y}, {self.z}, {self.dx}, {self.dy}, {self.dz})'
    
    def collide (self, other, rmin, rmax):
        """ return true if <self> and <other> collide in the future 
            and within the <rmin> - <rmax> coord range in X and Y """
        A = np.array([[self.dy, -self.dx], [other.dy, -other.dx]])
        det = np.linalg.det(A)
        if abs(det) < 1e-6:
            return None, False
        Ainv = np.linalg.inv(A)
        B = np.array([[self.d], [other.d]])
        X = np.matmul(Ainv, B)
        t1 = (X[0] - self.x) / self.dx
        t2 = (X[0] - other.x) / other.dx
        ans = t1[0] >= 0 and t2[0] >= 0 and rmin < X[0] and X[0] < rmax and rmin < X[1] and X[1] < rmax
        return ans, X
    
def is_int (X):
    vx = abs(X[0] - int(X[0]))
    vy = abs(X[1] - int(X[1]))
    return max(vx, vy) < 1e-8
        
xmin = 200000000000000
xmax = 400000000000000

# read data
hails = []
for line in lines:
    x = re.match(r'(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)', line)
    x = [int(x.group(i)) for i in range(1,7)]
    h = Hail(x[0], x[1], x[2], x[3], x[4], x[5])
    hails.append(h)

# part 1
from collections import defaultdict
colls = defaultdict(set)
count = 0
for i, h1 in enumerate(hails):
    for j, h2 in enumerate(hails[i+1:]):
        k = j + i + 1
        t, X = h1.collide(h2, xmin, xmax)
        if t:
            colls[i].add(k)
            count += 1
print(count)

# part 2

def cross_mat (v):
    return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

A = np.zeros((6,6))
B = np.zeros((6,))

h0 = hails[0]
h1 = hails[1]
h2 = hails[2]

B = np.hstack([- np.cross(h0.p, h0.v) + np.cross(h1.p, h1.v), - np.cross(h0.p, h0.v) + np.cross(h2.p, h2.v)])

M1 = cross_mat(h0.v) - cross_mat(h1.v)
M2 = cross_mat(h0.v) - cross_mat(h2.v)
M3 = -cross_mat(h0.p) + cross_mat(h1.p)
M4 = -cross_mat(h0.p) + cross_mat(h2.p)
A = np.vstack([np.hstack([M1, M3]), np.hstack([M2, M4])])
Ainv = np.linalg.inv(A)
C = np.matmul(Ainv, B)
ans = C[0] + C[1] + C[2]
print(ans)
# solution to part 2: 652666650475950

