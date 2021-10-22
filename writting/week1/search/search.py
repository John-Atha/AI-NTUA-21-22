import sys

class Node():
    def __init__(self, name, parent=None, estimation=0, time_added=0):
        self.name = name
        self.parent = parent
        self.estimation = estimation
        self.time_added = time_added
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        if self.parent:
            return f"{self.name}({self.estimation})<-{self.parent.name}({self.parent.estimation})"
        return f"{self.name}({self.estimation})"

    def print_with_path(self):
        curr = self
        print(f"{curr.name}({curr.estimation})", end='')
        if curr.name=='s':
            pass
        else:
            curr = curr.parent
            print('( <-', end='')
            while curr.name != 's':
                print(f"{curr.name}({curr.estimation})", '<-', end=' ')
                curr = curr.parent
            print(curr, end=' ), ')

    '''
    def __lt__(self, other):
        if not isinstance(other, Node):
            raise Exception("Second object is not of type Node.")
        if not other.estimation:
            return False
        if not self.estimation:
            return other
        return self.estimation < other.estimation
    '''
    
class Graph():
    def __init__(self):
        self.edges = dict()
        self.nodes = dict()
    
    def add_edge(self, u, v, weight):
        if self.edges.get(u):
            self.edges[u][v] = weight    
        else:
            self.edges[u] = dict()
            self.edges[u][v] = weight    

    def add_node(self, u):
        if u not in self.nodes:
            node = Node(name=u)
            self.nodes[u] = node

    def get_children(self, u):
        children = set()
        if self.edges.get(u):
            for v in self.edges[u]:
                children.add(v)
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
                for v in self.edges[node]:
                    print(f"{node} -> {v} : {self.edges[node][v]} ")

class Frontier():
    def __init__(self):
       self.frontier = []

    def empty(self):
        return len(self.frontier) == 0
    
    def add(self, node):
        self.frontier.append(node)

    def pop(self):
        if self.empty():
            raise Exception("Tried to remove node from empty frontier.")
        return self.frontier.pop()
    
    def __str__(self):
        return str([str(node) for node in self.frontier])
    
    def print_with_paths(self):
        print("Frontier:", end=' ')
        for node in self.frontier:
            node.print_with_path()
        print()

# by default, the init state has the label 's', and the goal state has the label 'g'
# we evaluate the next possible states only by the estimation value of the node
def hill_climbing_main(graph):

    visited = set()
    
    def hill_climbing_iter(best_node):
        print('--------------------------------------------------')
        if (best_node.name=='g'):
            print("I found the goal.")
            return

        prev = best_node
        children = graph.get_children(best_node)

        if (len(children)):
            for child in children:
                # if float(child.estimation) + float(graph.edges[prev][child]) < float(best_node.estimation):
                if float(child.estimation) < float(best_node.estimation):
                    best_node = child
        
        visited.add(prev.name)

        hill_climbing_logs(prev, best_node, children)

        if best_node != prev:
            hill_climbing_iter(best_node)
        else:
            return
    
    def hill_climbing_logs(prev, best_node, children):
        print("Current:", prev, end='  ---  ')
        print("Closed set:", visited, end='  ---  ')
        if best_node != prev:
            print("Children:", [str(child) for child in children], end='  ---  ')
            print(f"I am going to {best_node}")
        else:
            print("Children:", [str(child) for child in children], "  ---  No better children, no next state from", str(prev))
            print('--------------------------------------------------')
            print("Could not reach goal, local minimum at:", str(prev))

    print("I am hill climbing, in fact I do not use a frontier, so you will not find a frontier on my table:")
    hill_climbing_iter(graph.nodes.get('s'))


# we evaluate the next possible states only by the estimation value of the node
def best_first(graph):
    def best_first_logs(curr, frontier, children, expanded):
        print('-----------------------------------------')
        print(f"Current:", end=' ')
        curr.print_with_path()
        print(' --- ', end='')
        print("Closed set:", [str(node) for node in expanded], end=' --- ')
        print("Children:", [str(node) for node in children], end='\n')
        frontier.print_with_paths()

    def best_first_log_goal(curr):
        print('-----------------------------------------')
        print("Found goal 'g', with path:")
        curr.print_with_path()
        print()

    
    frontier = Frontier()
    expanded = set()
    time = 0

    curr = graph.nodes.get('s')
    curr.time_added = time
    frontier.add(curr)

    while not frontier.empty():
        
        curr = frontier.pop()
        
        if curr in expanded:
            continue
        if curr.name=='g':
            best_first_log_goal(curr)
            return
        
        time += 1
        children = graph.get_children(curr)
        for child in children:
            child_node = Node(name=child.name, estimation=child.estimation, parent=curr, time_added=time)
            frontier.add(child_node)
        
        expanded.add(curr)
        
        #frontier.frontier.sort(key=lambda node: (node.estimation+node.parent.estimation+graph.edges[node.parent][node]), reverse=True)
        frontier.frontier.sort(key=lambda node: (node.estimation, node.time_added), reverse=True)
        
        best_first_logs(curr, frontier, children, expanded)

    print("Could not find solution.")


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
        best_first(graph)
    elif way==3:
        pass
    else:
        print(f"Invalid way '{way}'\nJust type the corresponding number.")

solve()