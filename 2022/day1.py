import sys

input_file = sys.argv[1]

with open(input_file) as fh:
    lines = [a.strip() for a in fh.readlines()]

count = 0
max_counts = [0, 0, 0]

for line in lines:
    print(f'line = {line}')
    if line == '':
        print('closing')
        if count > max_counts[0]:
            max_counts[1:3] = max_counts[0:2]
            max_counts[0] = count
        elif count > max_counts[1]:
            max_counts[2] = max_counts[1]
            max_counts[1] = count
        elif count > max_counts[2]:
            max_counts[2] = count
        count = 0
    else:
        count += int(line)

print(max_counts)
print(sum(max_counts))