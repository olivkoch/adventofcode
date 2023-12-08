import sys
import functools 
from collections import defaultdict
import copy

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

hands = [x.split(' ')[0] for x in lines]
bids = [int(x.split(' ')[1]) for x in lines]

def hand_type(a):
    """ compute hand type. Input: string.  Output: integer """
    x = set([x for x in a])
    y = defaultdict(int)
    for b in a:
        y[b] += 1
    ym = max(y.values())
    xl = len(x)
    if ym == 5:
        return 0 # five of a kind
    if ym == 4:
        return 1 # four of a kind
    if ym ==3 and xl == 2:
        return 3 # full house
    if ym == 3:
        return 4 # three of a kind
    if xl == 3:
        return 5 # two pairs
    if xl == 4:
        return 6 # one pair
    if xl == 5:
        return 7 # high card
    assert(False)
    return 8

ranks = {'A':0, 'K':1, 'Q':2, 'J':3, 'T':4, '9':5,'8':6, '7':7, '6':8, '5':9, '4':10, '3':11, '2':12}

def sorted_by(a,b):
    """ compare two hands """
    if hand_type(a) < hand_type(b):
        return 1
    if hand_type(b) < hand_type(a):
        return -1
    for x in range(len(a)):
        if ranks[a[x]] < ranks[b[x]]:
            return 1
        if ranks[b[x]] < ranks[a[x]]:
            return -1
    return 0

cmp = functools.cmp_to_key(sorted_by)
orig_hands = copy.deepcopy(hands)
hands.sort(key=cmp)

ans = 0
for k,h in enumerate(hands):
    j = orig_hands.index(h)
    ans += (k+1) * bids[j]
print(ans)
