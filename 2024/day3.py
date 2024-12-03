import sys
import re

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]


out = 0
cmd = ''.join(lines)

cmd = re.sub(r'don\'t\(\).*?do\(\)', '', cmd)
m = re.findall(r'mul\((\d+),(\d+)\)', cmd)

if m:
    for x in m:
        out += int(x[0]) * int(x[1])

print(out)
