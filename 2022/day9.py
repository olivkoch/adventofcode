import sys
import math

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

xp = [0,0]
sps = [[0,0] for _ in range(9)]
positions = set()
positions.add(tuple(sps[-1]))

dir2vec = {'R': [1,0], 'L':[-1,0], 'U':[0,-1], 'D': [0,1]}

for line in lines:
    cmd = line.split(' ')
    direc = cmd[0]
    steps = int(cmd[1])
    for _ in range(steps):
        vec = dir2vec[direc]
        xp[0] += vec[0]
        xp[1] += vec[1]
        for k in range(9):
            sp = sps[k]
            hp = sps[k-1] if k > 0 else xp
            # update knot position
            if hp[0] == sp[0] and abs(hp[1]-sp[1]) >= 2:
                sp[1] += ((hp[1] - sp[1]) > 0) * 2 - 1
            elif hp[1] == sp[1] and abs(hp[0]-sp[0]) >= 2:
                sp[0] += ((hp[0] - sp[0]) > 0) * 2 - 1
            elif hp[0] != sp[0] and hp[1] != sp[1] and abs(hp[1]-sp[1]) + abs(hp[0]-sp[0]) >= 3:
                sp[1] += ((hp[1] - sp[1]) > 0) * 2 - 1
                sp[0] += ((hp[0] - sp[0]) > 0) * 2 - 1
            sps[k] = sp
        positions.add(tuple(sps[-1]))
    print(xp, sps)

print(len(positions))




