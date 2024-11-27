import sys

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

out  = 0

# for line in lines:
#     ln = int(len(line)/2)
#     dl = line[:ln]
#     dr = line[ln:]
#     x = set(dl).intersection(set(dr))
#     x = x.pop()
#     if x.isupper():
#         out += ord(x) - 65 + 27
#     else:
#         out += ord(x) - 97 + 1

# print(out)

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

for ls in divide_chunks(lines, 3):
    l1 = ls[0]
    l2 = ls[1]
    l3 = ls[2]
    x = set(l1).intersection(set(l2)).intersection(set(l3))
    x = x.pop()
    if x.isupper():
        out += ord(x) - 65 + 27
    else:
        out += ord(x) - 97 + 1

print(out)