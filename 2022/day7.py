import sys

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

def split_lines (lines):
    i = 0
    out = []
    cmd = []
    while i < len(lines):
        line = lines[i]
        if not line or line[0] == '$':
            out.append(cmd)
            cmd = [line]
            i += 1
            continue
        cmd.append(line)
        i += 1
    return out

cmds = split_lines (lines)

class Node:
    def __init__ (self, name, size = 0):
        self.name = name
        self.children = []
        self.parent = None
        self.size = size
        self.total_size = size

    def add_child (self, child):
        self.children.append(child)
        child.parent = self

head = Node('/')
curr = head

def process_cmd (curr, cmd):
    if cmd[0] == '$ ls':
        for f in cmd[1:]:
            if f[:3] == 'dir':
                n = Node (f.split(' ')[1])
            else:
                n = Node (f.split(' ')[1], int(f.split(' ')[0]))
            curr.add_child(n)
    elif cmd[0][:4] == '$ cd':
        if cmd[0] == '$ cd ..':
            curr = curr.parent
        else:
            tgt = cmd[0].split(' ')[2]
            cands = filter (lambda n: n.name == tgt, curr.children)
            curr = list(cands)[0]
    return curr

for cmd in cmds[2:]:
    curr = process_cmd (curr, cmd)

def compute_size_rec (node):
    if node.total_size == 0:
        node.total_size = sum([compute_size_rec(c) for c in node.children])
        return node.total_size
    return node.size

compute_size_rec (head)

def print_rec (node, depth):
    print('  ' * depth + node.name + f'[{node.total_size}]')
    for c in node.children:
        print_rec(c, depth + 1)

print_rec (head, depth=0)

def ls_rec (node, depth, out):
    out.append(node)
    for c in node.children:
        ls_rec(c, depth + 1, out)

s = []
ls_rec (head, depth=0, out=s)

# 1
# s = filter(lambda n : n.size == 0 and n.total_size < 100000, s)
# out = sum([x.total_size for x in s])
# print(out)

free_space = 70000000 - head.total_size

# 2
s = sorted (filter(lambda n : n.size == 0 and n.total_size > 30000000 - free_space, s), key = lambda n: n.total_size)
out = list(s)[0].total_size
print(out)
