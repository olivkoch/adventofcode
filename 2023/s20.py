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

class Broacaster:
    def __init__ (self, targets):
        self.name = 'broadcaster'
        self.targets = targets

    def run (self, pulse, source):
        return [(self.name, pulse, t) for t in self.targets]
    
class Button:
    def __init__(self):
        self.name = 'button'
        self.targets = ['broacaster']

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

for _, n in nodes.items():
    if type(n).__name__ == "Conjunction":
        for s in n.sources:
            n.mem[s] = False

# determine cycle length
period = 0
while True:

    stack = [(None, False, 'button')]

    count = 0
    while stack:
        nxt = stack.pop(0)
        if nxt[2] in nodes:
            cmd = nodes[nxt[2]].run(nxt[1], nxt[0])
            if cmd is None:
                continue
            stack += cmd
        count += 1

    period += 1
    if all_flipflops_off (nodes):
        break

print(f'{period=}')