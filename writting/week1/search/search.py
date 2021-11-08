import sys
import copy

class Node():
    def __init__(self, name, parent=None, estimation=0., time_added=0, path_distance=0.):
        self.name = name
        self.parent = parent
        self.estimation = float(estimation)
        self.time_added = time_added
        self.path_distance = float(path_distance)
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name

    def __hash__(self):
        curr = copy.deepcopy(self)
        path=self.name
        if curr.parent:
            curr = curr.parent
            while curr.parent:
                path+=curr.name
                curr = curr.parent
            path += 's'
        return hash(path)
    
    def __str__(self):
        if self.parent:
            return f"{self.name}({self.estimation})<-{self.parent.name}({self.parent.estimation})"
        return f"{self.name}({self.estimation})"

    def print_with_path(self, edges=dict()):
        curr = self
        if curr.path_distance:
            print(f"{curr.name}({curr.estimation}, {curr.path_distance})", end='')
        else:
            print(f"{curr.name}({curr.estimation})", end='')
        if curr.name=='s':
            pass
        else:
            if edges and edges.get(curr.parent.name).get(curr.name):
                print(f"(<-{edges[curr.parent.name][curr.name]}<-", end='')
            else:
                print(f"(<-", end='')
            curr = curr.parent
            while curr.name != 's':

                if edges and edges.get(curr.parent.name).get(curr.name):
                    print(f"{curr.name}({curr.estimation})", f"<-{edges[curr.parent.name][curr.name]}-", end='', sep='')
                else:
                    print(f"{curr.name}({curr.estimation})", "<-", end='', sep='')

                curr = curr.parent
            print(curr, end='), ')

class Graph():
    def __init__(self):
        self.edges = dict()
        self.nodes = dict()
    
    def add_edge(self, u, v, weight):
        if self.edges.get(u.name):
            self.edges[u.name][v.name] = float(weight)    
        else:
            self.edges[u.name] = dict()
            self.edges[u.name][v.name] = float(weight)    

    def add_node(self, u):
        if u not in self.nodes:
            node = Node(name=u)
            self.nodes[u] = node

    def get_children(self, u):
        children = set()
        if self.edges.get(u.name):
            for v in self.edges[u.name]:
                children.add(self.nodes[v])
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
            if self.edges.get(node.name):
                for v in self.edges[node.name]:
                    print(f"{node} -> {v} : {self.edges[node.name][v.name]} ")

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
    
    def print_with_paths(self, edges=dict()):
        print("Sorted frontier:", end=' ')
        print()
        for node in self.frontier:
            print('\t', end='')
            node.print_with_path(edges)
            print()
        print()

def hill_climbing_main(graph):
    '''
    * input: a `Graph` object
    * output: None
    * prints a table describing the visited states
    * by default, the init state has the label 's', and the goal state has the label 'g'
    * we evaluate the next possible states only by the node.estimation value
    * we do not keep a frontier, we just move on to a better child node, if there is one
    * the recursive method `hill_climbing_iter` is used to traverse the nodes
    * the method `hill_climbing_logs` prints the diagnostic messages
    '''
    visited = set()
    total_cost = 0

    def hill_climbing_iter(best_node):
        nonlocal total_cost
        print('--------------------------------------------------')
        if (best_node.name=='g'):
            print("I found the goal.")
            print("With total cost: ", total_cost)
            return
        # pick the best child node, if there is one better than current
        prev = best_node
        children = graph.get_children(best_node)
        if (len(children)):
            for child in children:
                if child.estimation < best_node.estimation:
                    best_node = child
        
        visited.add(prev.name)

        hill_climbing_logs(prev, best_node, children)

        if best_node != prev:
            total_cost += graph.edges[prev.name][best_node.name]
            hill_climbing_iter(best_node)
        else:
            # local minimum, stuck...
            return
    
    def hill_climbing_logs(prev, best_node, children):
        print("Current:", prev, end='\n')
        print("Closed set:", visited, end='\n')
        if best_node != prev:
            print("Children:", [str(child) for child in children], end='\n')
            print(f"I am going to {best_node}")
        else:
            print("Children:", [str(child) for child in children], "\nNo better children, no next state from", str(prev))
            print('--------------------------------------------------')
            print("Could not reach goal, local minimum at:", str(prev))
            print("With total cost: ", total_cost)

    print("I am hill climbing, in fact I do not use a frontier, so you will not find a frontier on my table:")
    hill_climbing_iter(graph.nodes.get('s'))

def best_first(graph):
    '''
    * input: a `Graph` object
    * output: None
    * prints a table describing the visited states
    * by default, the init state has the label 's', and the goal state has the label 'g'
    * we evaluate the next possible states only by the node.estimation value
    * we do keep a frontier, expanded by the current node's children at each time, to traverse the nodes
    * the methods `best_first_logs` and `best_first_log_goal` prints the diagnostic messages
    * the `time` variable is used to solve ties between nodes
    '''
    def best_first_logs(curr, frontier, children, expanded):
        print('-----------------------------------------')
        print(f"Current:", end=' ')
        curr.print_with_path()
        print('\n', end='')
        print("Closed set:", [str(node) for node in expanded], end='\n')
        print("Children:", [str(node) for node in children], end='\n')
        frontier.print_with_paths()

    def best_first_log_goal(curr):
        print('-----------------------------------------')
        print("Found goal 'g', with path:")
        curr.print_with_path()
        total_cost = 0
        while curr.parent:
            total_cost += graph.edges[curr.parent.name][curr.name]
            curr = curr.parent
        print('Total cost:', total_cost)

    
    frontier = Frontier()
    expanded = set()
    time = 0

    curr = graph.nodes.get('s')
    curr.time_added = time
    frontier.add(curr)

    while not frontier.empty():
        # pop and test...
        curr = frontier.pop()
        if curr in expanded:
            continue
        if curr.name=='g':
            best_first_log_goal(curr)
            return
        
        # expand...
        time += 1
        children = graph.get_children(curr)
        for child in children:
            child_node = Node(name=child.name, estimation=child.estimation, parent=curr, time_added=time)
            frontier.add(child_node)
        expanded.add(curr)

        # sort the frontier...
        frontier.frontier.sort(key=lambda node: (node.estimation, node.time_added), reverse=True)
        
        best_first_logs(curr, frontier, children, expanded)

    print("Could not find solution.")

def Astar(graph):
    '''
    * input: a `Graph` object
    * output: None
    * prints a table describing the visited states
    * by default, the init state has the label 's', and the goal state has the label 'g'
    * we evaluate the next possible states by the `estimation` + `path cost till here` values
    * we do keep a frontier, expanded by the current node's children at each time, to traverse the nodes
    * the methods `A_star_logs` and `A_Star_log_goal` prints the diagnostic messages
    * the `time` variable is used to solve ties between nodes
    '''

    def A_star_logs(curr, expanded, children, frontier):
        print('-----------------------------------------')
        print(f"Current:", end=' ')
        curr.print_with_path()
        print('\n', end='')
        print("Closed set:", [str(node) for node in expanded], end='\n')
        print("Children:", [str(node) for node in children], end='\n')
        frontier.print_with_paths(graph.edges)

    def A_Star_log_goal(curr):
        print('-----------------------------------------')
        print("Found goal 'g', with path:")
        curr.print_with_path()
        total_cost = 0
        while curr.parent:
            total_cost += graph.edges[curr.parent.name][curr.name]
            curr = curr.parent
        print('Total cost:', total_cost)

    frontier = Frontier()
    
    expanded = set()
    time = 0

    curr = graph.nodes.get('s')
    frontier.add(curr)

    while not frontier.empty():
        
        # pop and test...
        curr = frontier.pop()
        if curr in expanded:
            print(f"Current:", end=' ')
            curr.print_with_path()
            print('\n', end='')
            print("I have already seen that")
            continue
        elif curr.name=='g':
            A_Star_log_goal(curr)
            return
        
        # expand...
        time += 1
        children = graph.get_children(curr)
        for child in children:
            path_distance = curr.path_distance + graph.edges[curr.name][child.name]
            
            # if the node is already in the frontier with a worse value, remove it and add the new one
            # if the node is already in the frontier with a better value, do not add the new one (prunning)
            added_with_better_distance = False
            for node in frontier.frontier:
                if node.name==child.name and float(node.estimation)+node.path_distance>float(child.estimation)+path_distance:
                    frontier.frontier.remove(node)
                if node.name==child.name and float(node.estimation)+node.path_distance<float(child.estimation)+path_distance:
                    added_with_better_distance = True
                    break
            if not added_with_better_distance:
                child_node = Node(name=child.name, estimation=child.estimation, parent=curr, time_added=time, path_distance=path_distance)
                frontier.add(child_node)
            
        expanded.add(curr)

        # sort the frontier...
        frontier.frontier.sort(key=lambda node: (node.estimation+node.path_distance, node.time_added), reverse=True)

        A_star_logs(curr, expanded, children, frontier)

def all_paths(graph):

    def build_path(curr):
        path = ''
        cost = 0
        while curr.parent:
            path += f"{curr.name} <- "
            cost += graph.edges.get(curr.parent.name).get(curr.name)
            curr = curr.parent
        path += 's'
        path += f" with cost: {cost}"
        return path

    paths = set()

    frontier = Frontier()
    expanded = set()

    curr = graph.nodes.get('s')
    frontier.add(curr)

    while not frontier.empty():
        curr = frontier.pop()
        if curr.name == 'g':
            print("Found goal")
            path = build_path(curr)
            paths.add(path)
            continue
        if curr in expanded:
            continue
            
        children = graph.get_children(curr)
        for child in children:
            child_node = Node(name=child.name, estimation=child.estimation, parent=curr)
            frontier.add(child_node)
        
        expanded.add(curr)

    print("DFS is over")
    print("Total paths found:", len(paths))
    for path in paths:
        print(path)


def solve():
    '''
    * main def
    * builds the graph reading the input file
    * calls the selected method to find the solution
    '''
    graph = Graph()
    if len(sys.argv)!=2:
        sys.exit('Usage: python3 search.py <filename>') 
    graph.read_from_file(sys.argv[1])
    #graph.print()
    way = int(input('Which algorithm would you like to use (1, 2, 3 or 4)?\n  1.Hill Climbing\n  2.Best First\n  3.A*\n  4.DFS to count all paths from \'s\' to \'g\'\n'))
    if way==1:
        hill_climbing_main(graph)
    elif way==2:
        best_first(graph)
    elif way==3:
        Astar(graph)
    elif way==4:
        all_paths(graph)
    else:
        print(f"Invalid way '{way}'\nJust type the corresponding number.")

solve()
