import math

num_cells = 1000000
thresh = 36000000
s = [0 for _ in range(num_cells)]
found = False
for k in range(1, num_cells):
#for k in range(1,int(math.sqrt(num_cells))):
    for j in range(k, num_cells, k):
        s[j] += k*10
        if s[j] > thresh:
            print(f'found at {j}')
            found = True
            break
    if found:
        break
#print(s)


