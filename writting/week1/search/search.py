import sys
import math

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

    def get_children(self, u):
        children = set()
        if self.edges.get(u):
            for edge in self.edges.get(u):
                node = edge.get('child')
                children.add(node)
        return children
    
    def read_from_file(self, filename):
        with open(filename) as f:
            contents = f.read()
            if not contents.count('Edges:') or not contents.count('Estimations:'):
                raise Exception('Invalid input file.')
            contents = contents.splitlines()
            #print(contents)
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

# by default, the init state has the label 's', and the goal state has the label 'g'
def hill_climbing_main(graph):

    visited = set()
    
    def hill_climbing_iter(best_node):
        print('--------------------------------------------------')
        if (best_node.name=='g'):
            print("I found the goal.")
            return

        prev = best_node
        children = graph.get_children(best_node)
        best_node = Node(name='Dummy', estimation=math.inf)
        if (len(children)):
            for child in children:
                if float(child.estimation) < float(best_node.estimation):
                    best_node = child
        
        visited.add(prev.name)
        print("Current state:", prev, end='  ---  ')
        print("Closed set:", visited, end='  ---  ')
        if len(children):
            print("Children:", [str(child) for child in children], end='  ---  ')
            print(f"I am going to {best_node}")
            hill_climbing_iter(best_node)
        else:
            print("No children, no next state", str(prev))
            print('--------------------------------------------------')
            print("Could not reach goal, local minimum at:", str(prev))
            return
    
    print("I am hill climbing, in fact I do not use a frontier, so you will not find a frontier on my table:")
    hill_climbing_iter(graph.nodes.get('s'))
    

def solve():
    graph = Graph()
    if len(sys.argv)!=2:
        sys.exit('Usage: python3 search.py <filename>') 
    graph.read_from_file(sys.argv[1])
    #graph.print()
    way = int(input('Which algorithm would you like to use (1, 2 or 3)?\n  1.Hill Climbing\n  2.Best First\n  3.A*\n'))
    if way==1:
        hill_climbing_main(graph)
    elif way==2:
        pass
    elif way==3:
        pass
    else:
        print(f"Invalid way '{way}'\nJust type the corresponding number.")

solve()