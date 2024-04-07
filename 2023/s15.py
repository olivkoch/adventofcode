import sys
from collections import defaultdict

filename = sys.argv[1]

data = open(filename,'r').read()

xs = data.split(',')

# problem 1
# out = 0
# for x in xs:
#     print(x)
#     curr = 0
#     for c in x:
#         curr += ord(c)
#         curr *= 17
#         curr = curr % 256
#     out += curr

# print(out)

def hash(a):
    out = 0
    for c in a:
        out += ord(c)
        out *= 17
        out = out % 256
    return out


# problem 2
boxes = defaultdict(list)
for x in xs:
    if '=' in x:
        label,fl = x.split('=')
        id = hash(label)
        try:
            labels = list(map(lambda y:y[0], boxes[id]))
            idx = labels.index(label)
        except:
            idx = -1
        if idx == -1:
            boxes[id].append((label, fl))
        else:
            boxes[id][idx] = (label, fl)
    if '-' in x:
        label = x[:-1]
        id = hash(label)
        try:
            labels = list(map(lambda y:y[0], boxes[id]))
            idx = labels.index(label)
        except ValueError:
            idx = -1
        if idx != -1:
            boxes[id].pop(idx)

score = 0

for id, items in boxes.items():

    for i, item in enumerate(items):

        fl = int(item[1])

        score += (id+1) * (i+1) * fl

print(score)        


