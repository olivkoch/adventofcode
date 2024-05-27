import sys

filename = sys.argv[1]

with open(filename, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

print(lines)

bcast = []

def get_targets (line):
    return [a.strip() for a in line.split('->')[1].strip().split(',')]

def get_source (line):
    return line.split('->')[0].strip()[1:]

class FlipFlop:
    def __init__ (self, name, targets):
        self.name = name
        self.targets = targets
        self.mem = False

    def run(self, pulse, source):
        if pulse: # do nothing if high pulse
            return None
        self.mem = not self.mem
        out = self.mem
        return [(self.name, out, t) for t in self.targets]

class Conjunction:
    def __init__ (self, name, targets):
        self.name = name
        self.targets = targets
        self.mem = {}
        self.sources = []
    
    def __str__ (self):
        return f'[{self.name}] : {self.sources} -> {self.targets} {self.mem}'
    
    def run(self, pulse, source):
        self.mem[source] = pulse
        out = not (sum(self.mem.values()) == len(self.mem))
        return [(self.name, out, t) for t in self.targets]

class Dummy:
    def __init__(self, name):
        self.name = name
        self.targets = []

class Broacaster:
    def __init__ (self, targets):
        self.name = 'broadcaster'
        self.targets = targets

    def run (self, pulse, source):
        return [(self.name, pulse, t) for t in self.targets]
    
class Button:
    def __init__(self):
        self.name = 'button'
        self.targets = ['broadcaster']

    def run(self, pulse, source):
        return [(self.name, False, 'broadcaster')]
    
def all_flipflops_off (nodes):
    for _, n in nodes.items():
        if type(n).__name__ == "FlipFlop":
            if n.mem:
                return False
    return True

nodes = {}

nodes['button'] = Button()

for line in lines:
    if 'broadcaster' in line:
        nodes['broadcaster'] = Broacaster(get_targets(line))
    if line[0] == '%':
        nodes[get_source(line)] = FlipFlop(get_source(line), get_targets(line))
    if line[0] == '&':
        nodes[get_source(line)] = Conjunction(get_source(line), get_targets(line))
        
# populate conjunction states
for a, n in nodes.items():
    for x in n.targets:
        if x in nodes:
            nx = nodes[x]
            if type(nx).__name__ == "Conjunction":
                nx.sources.append(a)

def reset_states():
    for _, n in nodes.items():
        if type(n).__name__ == "Conjunction":
            for s in n.sources:
                n.mem[s] = False
        if type(n).__name__ == "FlipFlop":
            n.mem = False

# part 1: determine cycle length
# period = 0
# p_per_period = [0,0]
# run = 0

# while True:

#     stack = [(None, False, 'button')]
#     run+= 1
#     while stack:
#         nxt = stack.pop(0)
#         if nxt[0]:
#             p_per_period[1 if nxt[1] else 0]+= 1
#             break
#         if nxt[2] in nodes:
#             cmd = nodes[nxt[2]].run(nxt[1], nxt[0])
#             if cmd is None:
#                 continue
#             stack += cmd

#     period += 1
#     if all_flipflops_off (nodes) or run == 1000: # part 1
#         break

# part 1
# num = 1000 / period
# ans = p_per_period[0] * num * p_per_period[1] * num
# print(f'{period=}, {p_per_period=}, {run=}, {ans=}')

# part 2
ans = []
for dep in ['pb', 'dj', 'rr', 'nl']:

    reset_states()
    
    run = 0
    done = False

    while True:

        stack = [(None, False, 'button')]
        run += 1
        while stack:
            nxt = stack.pop(0)
            if nxt[0] == dep and not nxt[1]:
                done = True
                break
            if nxt[2] in nodes:
                cmd = nodes[nxt[2]].run(nxt[1], nxt[0])
                if cmd is None:
                    continue
                stack += cmd

        if done:
            break

    print(f'[{dep}] {run=}')
    ans.append(run)

ans = ans[0] * ans[1] * ans[2] * ans[3]
print(ans)

# code to display a network - do not modify this cell
# from graphviz import Digraph
# def trace(root, _nodes):
#     nodes, edges = set(), set()
#     def build(v):
#         if v not in nodes:
#             nodes.add(v)
#             for child_name in v.targets:
#                 if child_name in _nodes:
#                     child = _nodes[child_name]
#                     edges.add((v, child))
#                     build(child)
#                 else:
#                     print(f'warning: {child_name} not found in _nodes')
#                     dummy = Dummy(child_name)
#                     edges.add((v, dummy))
#                     build(dummy)
#     build(root)
#     return nodes, edges

# def draw_dot(root, _nodes, format='svg', rankdir='LR'):
#     """
#     format: png | svg | ...
#     rankdir: TB (top to bottom graph) | LR (left to right)
#     """
#     assert rankdir in ['LR', 'TB']
#     nodes, edges = trace(root, _nodes)
#     dot = Digraph(format=format, graph_attr={'rankdir': rankdir}) #, node_attr={'rankdir': 'TB'})
    
#     layer_colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFCC99", "#99CCFF"]
    
#     for n in nodes:
#         color = layer_colors[0] if type(n).__name__ == "Conjunction" else layer_colors[1]
#         dot.node(name=str(id(n.name)), label="{ %s }" % (n.name), shape='record', style='filled', color=color)
    
#     for n1, n2 in edges:
#         dot.edge(str(id(n1.name)), str(id(n2.name)))
    
#     return dot

# g = draw_dot(nodes['button'], nodes)
# g.render('file', format='png')