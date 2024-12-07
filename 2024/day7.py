import sys
from collections import defaultdict
import operator

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

ops = {
    '+': operator.add,
    '*': operator.mul,
    '||': lambda u,v : int(str(v)+str(u))
}

def to_numbers (vec):
    assert(vec)
    if len(vec) == 1:
        return [f'{vec[0]}']
    s1 = [f"ops['+']({vec[0]},{a})" for a in to_numbers(vec[1:])]
    s2 = [f"ops['*']({vec[0]},{a})" for a in to_numbers(vec[1:])]
    s3 = [f"ops['||']({vec[0]},{a})" for a in to_numbers(vec[1:])]
    return s1 + s2 + s3

out = 0
for i, line in enumerate(lines):
    print(i, len(lines))
    res = int(line.split(':')[0])
    ds = [int(a) for a in line.split(':')[1].strip().split(' ')][::-1]
    xs = to_numbers(ds)
    for x in xs:
        if eval(x) == res:
            out += res
            break 
print(out)   
