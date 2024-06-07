import sys
import copy
from PIL import Image
import numpy as np

stoi = {'>': 2, '<':3, '^':4, 'v':5}

filename = sys.argv[1]

data = [a.strip() for a in open(filename, 'r').readlines()]

def arr_to_png(mp, filename, scale=1.0):
    rows, cols = len(mp), len(mp[0])
    arr = np.zeros((rows, cols), dtype=np.int32)
    im = Image.fromarray(arr).convert('RGB')
    pixels = im.load()
    h = im.size[1]
    for r,line in enumerate(mp):
        for c,u in enumerate(line):
            if u == 1:
                pixels[c, r] = (255, 255, 255)
            if u == 6:
                pixels[c,r] = (255, 0, 0)
            if u == 7:
                pixels[c,r] = (255, 0, 255)
    im = im.resize((int(cols*scale), int(rows*scale)), Image.Resampling.LANCZOS)
    im.save(filename)
    return im

def data_to_array (data):
    """ convert map as strings into a 2D array """
    rows = len(data)
    cols = len(data[0])
    mp = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if data[r][c] == '#':
                mp[r][c] = 1
                continue
            if data[r][c] == '.':
                continue
            mp[r][c] = stoi[data[r][c]]
    return mp


class Node:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.neigh = [] # a list of Node
        self.m_neigh = [] # marked neighbors during graph building
        self.dist = 0 # max distance from source
        self.edges = [] # a list of Edge
        self.name = f'({self.r}, {self.c})'
        self.targets = [] # neighbors in part 2's network

    def __str__ (self):
        ns = ','.join([f'({n.r}, {n.c})' for n in self.neigh])
        return f'({self.r}, {self.c}) [{ns}]'

class Path:
    def __init__(self, sta): # sta is a Node not a tuple
        self.nodes = [sta]
        self.visited = set()
        self.visited.add((sta.r, sta.c))
        self.is_alive = True

    def next_nodes (self, nodes):
        cur = self.nodes[-1]
        ns = filter (lambda u: not self.is_visited (u), cur.neigh)
        return list(ns)
    
    def extend (self, node):
        self.nodes.append(node)
        self.visited.add((node.r, node.c))

    def is_visited (self, node):
        return (node.r, node.c) in self.visited

    def last_pos (self):
        n = self.nodes[-1]
        return (n.r, n.c)
    
    def __str__ (self):
        return ' -> '.join ([f'({n.r}, {n.c})' for n in self.nodes])

class Edge:
    def __init__(self, a, b, len):
        self.a = a # a Node
        self.b = b # a Node
        self.len = len
        self.visited = False

    def __str__ (self):
        return f'E -- {str(self.a)} -- {str(self.b)}'
    
    def other (self, c):
        return self.b if c == self.a else self.a
    
    # def __eq__ (self, other):
    #     return (self.a == other.a and self.b == other.b) or (self.a == other.b) and (self.b == other.a)

def copy_path (p):
    s = Path(p.nodes[0])
    s.visited = copy.copy(p.visited)#copy.deepcopy(p.visited)
    s.is_alive = p.is_alive
    s.nodes = copy.copy(p.nodes) #copy.deepcopy(p.nodes)
    return s

def array_to_nodes (arr):
    """ convert a 2D map into a graph of nodes """
    nodes = {}
    rows = len(arr)
    cols = len(arr[0])
    for r in range(rows):
        for c in range(cols):
            if arr[r][c] != 1:
                nodes[(r,c)] = Node(r, c)
    for node in nodes.values():
        r = node.r
        c = node.c
        if r > 0:
            if arr[r-1][c] != 1:# and arr[r-1][c] != stoi['v']:
                node.neigh.append(nodes[(r-1,c)])
        if r < rows - 1:
            if arr[r+1][c] != 1:# and arr[r+1][c] != stoi['^']:
                node.neigh.append(nodes[(r+1,c)])
        if c > 0:
            if arr[r][c-1] != 1:# and arr[r][c-1] != stoi['>']:
                node.neigh.append(nodes[(r,c-1)])
        if c < cols - 1:
            if arr[r][c+1] != 1:# and arr[r][c+1] != stoi['<']:
                node.neigh.append(nodes[(r,c+1)])
    return nodes

def find_all_paths (nodes, sta, end):
    """ find longest path in the graph """
    paths = [Path(nodes[sta])]
    done = False
    count = 0
    while not done:# and count < 25:
        count += 1
        done = True
        new_paths = []
        for pth in paths:
            if pth.is_visited(nodes[end]):
                continue
            ns = pth.next_nodes(nodes)
            if ns:
                done = False
                if len(ns) == 1:
                    pth.extend(ns[0])
                else:
                    nps = [copy_path(pth) for _ in range(len(ns))]
                    for i, n in enumerate(ns):
                        nps[i].extend(n)
                    new_paths += nps
                    pth.is_alive = False
        paths += new_paths
        paths = list(filter(lambda u: u.is_alive, paths))
    return paths

def find_longest_path_brute_force (nodes, sta, end):

    paths = find_all_paths (nodes, sta, end)

    # only keep paths ending at the exit
    paths = list(filter (lambda p: p.last_pos() == (end), paths))

    paths = sorted(paths, key = lambda p: len(p.nodes))

    if paths:
        return paths[-1]
    return None

def find_unfinished_node (nodes):
    for n in nodes:
        if len(n.m_neigh) < len(n.neigh):
            return n
    return None

def find_next_unmarked_neighbor (n):
    assert (len(n.m_neigh) < len(n.neigh))
    a = set(n.neigh) - set(n.m_neigh)
    return list(a)[0]

def build_graph (nodes, sta, end):
    """ convert the nodes into a graph """
    # find intersections
    its = list(filter(lambda n: len(nodes[n].neigh) > 2, nodes.keys())) + [sta, end]
    its = list(map (lambda u : nodes[u], its))
    print(f'{len(its)} intersections')
    V = set()
    E = set()
    # follow all unseen paths between intersections
    while True:
        n = find_unfinished_node (its)
        if not n:
            break
        p = find_next_unmarked_neighbor (n)
        # follow path until next intersection
        pth = [n, p]
        pti = {n, p}
        while True:
            s = list(filter(lambda u: not u in pti, pth[-1].neigh))
            assert(len(s)==1)
            if not s[0] in its:
                pth.append(s[0])
                pti.add(s[0])
            else:
                n.m_neigh.append(p)
                s[0].m_neigh.append(pth[-1])
                pth.append(s[0])
                break
        v1 = pth[0]  
        v2 = pth[-1] 
        ed = Edge(v1, v2, len(pth) - 1)
        v1.targets.append(v2)
        v2.targets.append(v1)
        if not v1 in V:
            V.add(v1)
        if not v2 in V:
            V.add(v2)
        E.add(ed)
        v1.edges.append(ed)
        v2.edges.append(ed)
    print(f'{len(V)} vertices, {len(E)} edges')
    return V, E

import random
from collections import defaultdict

def find_one_path (V, E, nodes, sta, end):
    tov = defaultdict(set) # list of edges pointing to a given node
    for e in E:
        e.visited = False
        tov[e.a].add(e)
        tov[e.b].add(e)
    prev = None
    curr = nodes[sta]
    failed = False
    len = 0
    while curr != nodes[end]:
         # forbid return to prev
        if prev:
            for u in tov[prev]:
                u.visited = True
        # pick next node
        eds = list(filter(lambda u: not u.visited, curr.edges))
        if not eds:
            failed = True
            break
        edo = random.choice(eds)
        prev = curr
        curr = edo.other(curr)
        len += edo.len
#    print(f'{failed=}, {len=}')
    return failed, len

def find_longest_path (V, E, nodes, sta, end):
    max_len = 0
    while True:
        failed, len = find_one_path(V, E, nodes, sta, end)
        if not failed and len > max_len:
            print(max_len)
            max_len = len
    print(max_len)

# main 

sta = (0, data[0].index('.'))
end = (len(data) - 1, data[-1].index('.'))

arr = data_to_array (data)

nodes = array_to_nodes (arr)

degree = sum([len(n.neigh) for n in nodes.values()])/len(nodes)

# part 1: brute force
# pth = find_longest_path_brute_force (nodes, sta, end)
# print (f'longest path: {len(pth.nodes)}')

# part 2: build a graph with intersections as vertices 
# then search for longest path in the graph
V, E = build_graph (nodes, sta, end)

its = list(filter(lambda n: len(nodes[n].neigh) > 2, nodes.keys())) + [sta, end]
for n in its:
    arr[n[0]][n[1]] = 7

arr_to_png (arr, f'day-23-{len(arr)}.png')

find_longest_path (V, E, nodes, sta, end)


# code to display a network - do not modify this cell

from graphviz import Digraph
def trace(root, _nodes):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v.targets:
                edges.add((v, child))
                build(child)
            #else:
            #    print(f'warning: {child} not found in _nodes')
                #dummy = Dummy(child_name)
                #edges.add((v, dummy))
                #build(dummy)
    build(root)
    return nodes, edges

def draw_dot(root, _nodes, format='svg', rankdir='LR'):
    """
    format: png | svg | ...
    rankdir: TB (top to bottom graph) | LR (left to right)
    """
    assert rankdir in ['LR', 'TB']
    nodes, edges = trace(root, _nodes)
    dot = Digraph(format=format, graph_attr={'rankdir': rankdir}) #, node_attr={'rankdir': 'TB'})
    
    layer_colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFCC99", "#99CCFF"]
    
    for n in nodes:
        color = layer_colors[0]# if type(n).__name__ == "Conjunction" else layer_colors[1]
        dot.node(name=str(id(n.name)), label="{ %s }" % (n.name), shape='record', style='filled', color=color)
    
    for n1, n2 in edges:
        dot.edge(str(id(n1.name)), str(id(n2.name)))
    
    return dot

g = draw_dot(nodes[sta], nodes)
g.render('file', format='png')