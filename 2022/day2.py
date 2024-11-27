import sys

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

mapper = {}
# A = Rock, B = Paper, C = Scissors
# X = Rock, Y = Paper, Z = Scissors
mapper['A X'] = 3
mapper['A Y'] = 4
mapper['A Z'] = 8
mapper['B X'] = 1
mapper['B Y'] = 5
mapper['B Z'] = 9
mapper['C X'] = 2
mapper['C Y'] = 6
mapper['C Z'] = 7

score = 0
for line in lines:
    score += mapper[line]

print(score)
