import math

num_cells = 1000000
thresh = 36000000
s = [0 for _ in range(num_cells)]
found = False
for k in range(1, num_cells):
#for k in range(1,int(math.sqrt(num_cells))):
    kk = 0
    for j in range(k, num_cells, k):
        s[j] += k*11
        kk += 1
        if kk == 50:
            break
        if s[j] > thresh:
            print(f'found at {j}')
            found = True
            break
    if found:
        break
#print(s)


