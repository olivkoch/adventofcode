import sys
import functools 
from collections import defaultdict
import copy

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [x.strip() for x in fh.readlines()]

hands = [x.split(' ')[0] for x in lines]
bids = [int(x.split(' ')[1]) for x in lines]

def count_pairs(y):
    """ y is a dict card type -> number of cards of that type """
    s = y.values()
    return sum([x == 2 for x in s])

def hand_type(a):
    """ compute hand type. Input: string.  Output: integer """
    x = set([x for x in a])
    y = defaultdict(int)
    for b in a:
        y[b] += 1
#    print(a)
#    print(y)
    if not a: # empty hand
        return 6
    ym = max(y.values())
    xl = len(x)
    if ym == 5:
        return 0 # five of a kind
    if ym == 4:
        return 1 # four of a kind
    if ym ==3 and xl == 2:
        return 2 # full house
    if ym == 3:
        return 3 # three of a kind
    if count_pairs(y) == 2:
        return 4 # two pairs
    if count_pairs(y) == 1:
        return 5 # one pair
    return 6 # high card
    
def map_from_j (t):
    """ what the best type can be given input type t and one J in the deck """
    if t == 1: # four of a kind becomes five of a kind
        return 0
    if t == 2:
        return 1
    if t == 3:
        return 1
    if t == 4:
        return 2
    if t == 5:
        return 3
    if t == 6:
        return 5
    return t 
    
def best_type(h):
    js = sum([x == 'J' for x in h])
    t = hand_type(h.replace('J',''))
    for _ in range(js):
        t = map_from_j (t)
    return t

ranks = {'A':0, 'K':1, 'Q':2, 'T':4, '9':5,'8':6, '7':7, '6':8, '5':9, '4':10, '3':11, '2':12, 'J':13}

def sorted_by(a,b):
    """ compare two hands """
    if best_type(a) < best_type(b):
        return 1
    if best_type(b) < best_type(a):
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

print(hands)

ans = 0
for k,h in enumerate(hands):
    j = orig_hands.index(h)
    ans += (k+1) * bids[j]
print(ans)
