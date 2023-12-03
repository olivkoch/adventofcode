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
    for st in sets:
        for color, max_it in zip(colors, max_items):
            #print(f'color = {color}')
            m = re.search(f'(\d+) {color}', st)
            if m is not None:
                num_it = int(m.group(1))
             #   print(num_it)
                if num_it > max_it:
                    failed = True
              #      print('\tfailed')
                    break
        if failed:
            break
    if not failed:
        ans += gid
print(ans)
