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

# class Vertex:
#     def __init__(self, node):
#         self.node = node
#         self.edges = []

#     def __str__ (self):
#         return str(self.node)

class Edge:
    def __init__(self, a, b, len):
        self.a = a
        self.b = b
        self.len = len

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
        # print(f' ******** paths {len(paths)} ************')
        # for pth in paths:
        #     print(pth)
    return paths

def find_longest_path (nodes, sta, end):

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
        if not v1 in V:
            V.add(v1)
        if not v2 in V:
            V.add(v2)
        E.add(ed)
    print(f'{len(V)} vertices, {len(E)} edges')
    return V, E


# main 

sta = (0, data[0].index('.'))
end = (len(data) - 1, data[-1].index('.'))

arr = data_to_array (data)

nodes = array_to_nodes (arr)

degree = sum([len(n.neigh) for n in nodes.values()])/len(nodes)

V, E = build_graph (nodes, sta, end)

its = list(filter(lambda n: len(nodes[n].neigh) > 2, nodes.keys())) + [sta, end]
for n in its:
    arr[n[0]][n[1]] = 7

arr_to_png (arr, f'day-23-{len(arr)}.png')