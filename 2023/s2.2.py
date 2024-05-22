import re

filename = '2.dat'
with open(filename,'r') as fh:
    lines = fh.readlines()

ans = 0
colors = ['red', 'green', 'blue']
max_items = [12, 13, 14]

for line in lines:
    line = line.strip()
    print(line)
    # read game id
    m = re.match(r'Game (\d+):(.*)', line)
    print(m.group(1))
    gid = int(m.group(1))
    # read game sets
    sets = m.group(2).split(';')
    print(sets)
    failed = False
    max_colors = {c:0 for c in colors}
    for st in sets:
        for k, color in enumerate(colors):
            #print(f'color = {color}')
            m = re.search(f'(\d+) {color}', st)
            if m is not None:
                num_it = int(m.group(1))
                max_colors[color] = max([max_colors[color], num_it])
#    print(max_colors)
    vals = list(max_colors.values())
    ans += vals[0] * vals[1] * vals[2]
print(ans)
