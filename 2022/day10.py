import sys

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

tp = ['addx' in x for x in lines]
vp = [int(x.split(' ')[1]) if u else 0 for u, x in zip(tp, lines)]

for cycle in [260]:#, 60, 100, 140, 180, 220]:
    c = 0
    reg = 1
    crt = 0
    out = ''
    for t, v in zip(tp, vp):
        if not t:
            if crt in [reg-1, reg, reg+1]:
                out += '#'
            else:
                out += '.'
            crt += 1
            if crt == 40:
                crt = 0
                out += '\n'
        else:
            if crt in [reg-1, reg, reg+1]:
                out += '#'
            else:
                out += '.'
            crt += 1
            if crt == 40:
                crt = 0
                out += '\n'
            if crt in [reg-1, reg, reg+1]:
                out += '#'
            else:
                out += '.'
            crt += 1
            if crt == 40:
                crt = 0
                out += '\n'
        c += 2 if t else 1
        if c >= cycle:
            break
        if c <= cycle:
            reg += v
    print(out)
