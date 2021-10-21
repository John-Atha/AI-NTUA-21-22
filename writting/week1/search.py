import sys

class Node():
    def __init__(self, name, parent=None, estimation=None):
        self.name = name
        self.parent = parent
        self.estimation = estimation
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return f"{self.name}({self.estimation})"

class Graph():
    def __init__(self):
        self.edges = dict()
        self.nodes = dict()
    
    def add_edge(self, u, v, weight):
        if self.edges.get(u):
            self.edges[u].append({ 'child': v, 'weight': weight, })
        else:
            self.edges[u] = [{ 'child': v, 'weight': weight, }]
    
    def add_node(self, u):
        if u not in self.nodes:
            node = Node(name=u)
            self.nodes[u] = node

    def get_neighbours(self, u):
        return self.edges.get(u)
    
    def read_from_file(self, filename):
        with open(filename) as f:
            contents = f.read()
            if not contents.count('Edges:') or not contents.count('Estimations:'):
                raise Exception('Invalid input file.')
            contents = contents.splitlines()
            print(contents)
            estimations_started = False
            for line in contents:
                if 'Edges:' in line:
                    continue
                if 'Estimations:' in line:
                    estimations_started = True
                    continue
                if not estimations_started:
                    line = line.split(' ')
                    u, v, weight = line
                    self.add_node(u)
                    self.add_node(v)
                    self.add_edge(self.nodes[u], self.nodes[v], weight)
                else:
                    line = line.split(' ')
                    u, estimation = line
                    self.add_node(u)
                    self.nodes[u].estimation = estimation
              
    def print(self):
        print("Current Graph state:")
        for u in self.nodes:
            node = self.nodes[u]
            if self.edges.get(node):
                for edge in self.edges[node]:
                    print(f"{node} -> {edge.get('child')} : {edge.get('weight')} ")

class Frontier():
    def __init__(self):
       self.frontier = []

    def empty(self):
        return len(self.frontier) == 0
    
    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        if self.empty():
            raise Exception("Tried to remove node from empty frontier.")

def solve():
    graph = Graph()
    if len(sys.argv)!=2:
        sys.exit('Usage: python3 search.py <filename>') 
    graph.read_from_file(sys.argv[1])
    graph.print()
    way = int(input('Which algorithm would you like to use (1, 2 or 3)?\n  1.Hill Climbing\n  2.Best First\n  3.A*\n'))
    if way==1:
        pass
    elif way==2:
        pass
    elif way==3:
        pass
    else:
        print(f"Invalid way '{way}'\nJust type the corresponding number.")

solve()