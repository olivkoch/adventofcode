import sys
import re
import heapq
from collections import defaultdict

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

data = lines[0]

disk = ''
id = 0
pos = 0

taken = []
free = []

# part 1
# for i, c in enumerate(data):
#     x = int(c)
#     if i % 2 == 1:
#         disk += '.' * x
#         for _ in range(x):
#             free.append(pos)
#             pos += 1
#     else:
#         for _ in range(x):
#             taken.append((pos,id))
#             pos += 1
#         disk += f'{id}' * x
#         id += 1

# taken2 = []
# # move files
# while free:
#     q = free.pop(0)
#     t = taken.pop()
#     if t[0] < q:
#         taken.append(t)
#         break
#     taken2.append((q,t[1]))

# out = 0
# for k in taken:
#     out += k[0] * k[1]
# for k in taken2:
#     out += k[0] * k[1]
# print(out)

# part 2
files = []
free = defaultdict(list)
id = 0
for i, c in enumerate(data):
    x = int(c)
    if i % 2 == 1:
        free[x].append(pos)
        pos += x
    else:
        files.append((pos, x, id))
        pos += x
        id += 1

files2 = []

while files:
    # try to move right-most file to the left
    q = files.pop()
    q_pos = q[0]
    width = q[1]
    # find best available slot
    best_pos = None
    best_width = None
    for w in range(width, 10):
        if w in free and free[w]:
            pos = heapq.heappop(free[w])
            if pos < q_pos and (best_pos is None or pos < best_pos):
                best_pos = pos
                best_width = w
            heapq.heappush(free[w], pos)
    if best_pos:
        heapq.heappop(free[best_width])
        new_width = best_width - width
        if new_width > 0:
            heapq.heappush(free[new_width], best_pos + width)
        files2.append((best_pos, q[1], q[2]))
    else:
        files2.append(q)

out = 0
for x in files2:
    for k in range(x[0], x[0] + x[1]):
        out += k * x[2]
print(out)
