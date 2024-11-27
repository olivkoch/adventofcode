import sys

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

data = lines[0]

#data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
#data = 'bvwbjplbgvbhsrlpgdmjqwftvncz'

for c in range(len(data) - 14):
    x = data[c:c+14]
    if len(set(x)) == 14:
        print(c + 14)
        break

# i = 0
# for l1, l2, l3, l4 in zip(data, data[1:], data[2:], data[3:]):
#     if len(set([l1, l2, l3, l4])) == 4:
#         print(i+4)
#         break
#     i += 1

