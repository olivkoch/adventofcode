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
 
def print_blocks(blocks):
    for k,v in blocks.items():
        for u in v:
            print(u)
        print()

def slide_north(blocks):
    nl = len(blocks)
    nc = len(blocks[0])
    out = [[x for x in line] for line in blocks]
    for i in range(1,nl):
        for j in range(nc):
            if out[i][j] == 'O':
                k = i
                while k > 0 and out[k-1][j] == '.':
                    k -= 1
                if k < i:
                    out[k][j] = 'O'
                    out[i][j] = '.'
    out = [''.join(line) for line in out]
    return out
                
def rotate_clockwise(blocks):
    nl = len(blocks)
    nc = len(blocks[0])
    out = [[blocks[nl-1-i][j] for i in range(nl)] for j in range(nc)]
    out = [''.join(line) for line in out]
    return out

def cycle(blocks):
    out = slide_north(blocks)
    out = rotate_clockwise(out) # west
    out = slide_north(out)
    out = rotate_clockwise(out) # south
    out = slide_north(out)
    out = rotate_clockwise(out) # east
    out = slide_north(out)
    out = rotate_clockwise(out)
    return out
    
def compute_load(blocks):
    out = 0
    nl = len(blocks)
    for i,line in enumerate(blocks):
        for c in line:
            if c == 'O':
                out += nl - i
    return out

def same_blocks(a,b):
    for x,y in zip(a,b):
        if x != y:
            return False
    return True

def main():
    filename = sys.argv[1]
    blocks = read_data(filename)
    print_blocks(blocks)
    out = 0
    period = 154 # hard-coded, found during first pass with brute-force search
    remain = 1000000000 % period
    for _,v in blocks.items():
        viewed = []
        # # use this code to find the period
        # for c in range(10000):
        #     if sum([same_blocks(y, v) for y in viewed]) > 0:
        #         print(f'already viewed at cycle {c}')
        #         break
        #     viewed.append(v)
        #     v = cycle(v)
        for c in range(period + remain):
            v = cycle(v)
        out += compute_load(v)
    print(out)

if __name__ == "__main__":
    main()
