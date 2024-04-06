import math as m
import sys
import re
from itertools import product

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [line.strip() for line in fh.readlines()]

maxi = 0
for line in lines:
    x = list(filter(lambda y: y=='?', line))
    maxi = max([maxi, len(x)])

def is_valid(st, counts):
    assert ('?' not in st)
    m = re.findall(r'(\#+)', st)
    if m is None:
        return False
    x = [len(a) for a in m]
    if len(x) != len(counts):
        return False
    return (sum([x[i] != counts[i] for i in range(len(x))]) == 0)

def parse_line(line):
    a = line.split(' ')[0]
    b = [int(x) for x in line.split(' ')[1].split(',')]
    return a, b

def yield_all_possible_strings (st):
    x = []
    for c in st:
        if c == '?':
            x.append(['.','#'])
        else:
            x.append([c])
    return [''.join(a) for a in product(*x)]


if False:
    line  = '.###.##.#... 3,2,1'
    st, counts =parse_line(line)
    v = is_valid(st, counts)
    print(v)


if False:
    line  = '.###.#?.#..? 3,2,1'
    st, counts =parse_line(line)
    for a in yield_all_possible_strings(st):
        print(a)

def count_valid_brute_force (st, counts):
    ans = 0
    for x in yield_all_possible_strings(st):
        if is_valid(x, counts):
            ans += 1
    return ans

def flatten (xss):
    """ flatten a list of list """
    return [x for xs in xss for x in xs ]

def count_valid_dp (st, counts):
    # hack: add a valid spring at the beginning and at the end
    st = '.' + st + '.'
    flags = flatten([[True] * k + [False] for k in counts])
    flags = [False] + flags
    n = len(st)
    m = len(flags)
    dp = [ [0 for _ in range(m+1)] for _ in range(n+1)]
    dp[n][m] = 1
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            c = st[i]
            if c == '#':
                damaged = True
                operational = False
            elif c == '.':
                damaged = False
                operational = True
            elif c == '?':
                damaged = True
                operational = True
            sum = 0
            if damaged and flags[j]:
                sum += dp[i+1][j+1]
            elif operational and not flags[j]:
                sum += dp[i+1][j+1] + dp[i+1][j]
            dp[i][j] = sum
    return dp[0][0]


if True:
    ans = 0
    for line in lines:
        st, counts =parse_line(line)
        st = '?'.join([st] * 5)
        counts = counts * 5
        ans += count_valid_dp (st, counts)
    print(ans)


#line = '?#?#?#?#?#?#?#?'
#counts = (1,3,1,6)
#line = '?'.join(['.??..??...?##.'] * 5)
#counts = (1,1,3) * 5
#ans = count_valid_dp(line, counts)
#print(ans)
