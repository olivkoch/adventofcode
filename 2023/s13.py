import sys
from collections import defaultdict


def read_data(filename):
    filename = sys.argv[1]
    with open(filename, 'r') as fh:
        lines = [x.strip() for x in fh.readlines()]
    blocks = defaultdict(list)
    i = 0
    for line in lines:
        if not line:
            i += 1
            continue
        blocks[i].append(line)
    return blocks

def is_symetric(line, split):
    """ return True if the split creates a symetry """
    a = line[:split]
    b = line[split:]
    c = min([len(a), len(b)])
    a = a[::-1][:c]
    b = b[:c]
    return a == b

def diff(line, split):
    """ count the string distance at split """
    a = line[:split]
    b = line[split:]
    c = min([len(a), len(b)])
    a = a[::-1][:c]
    b = b[:c]
    out = sum([x!=y for (x,y) in zip(a,b)])
    return out

def find_vertical_split(blocks, debug=False):
    nc = len(blocks[0])
    for i in range(1,nc):
        score = 0
        for block in blocks:
            score += diff(block, i)
        if score == 1:
            return i
    return -1

def transpose_blocks(blocks):
    n = len(blocks)
    m = len(blocks[0])
    return [[blocks[j][i] for j in range(n)] for i in range(m)]
 
def print_blocks(blocks):
    for k,v in blocks.items():
        for u in v:
            print(u)
        print()

def main():
    filename = sys.argv[1]
    blocks = read_data(filename)
    print_blocks(blocks)
    out = 0
    for k,v in blocks.items():
        a = find_vertical_split(v)
        if a>0: out += a; print(f'found vertical split at {a}')
        if a == -1:
            b = find_vertical_split(transpose_blocks(v))
            if b>0: out += 100 * b; print(f'found horizontal split at {b}')
    print(out)
   # a = find_vertical_split(blocks)
   

if __name__ == "__main__":
    main()
