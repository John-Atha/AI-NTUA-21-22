import sys
import copy

def flatten_2d(l):
    return [item for sublist in l for item in sublist]

def get_id_from_node_str(node):
    if 'mini' in node:
        return int(node.replace('mini', '').replace('-', ''))
    if 'maxi' in node:
        return int(node.replace('maxi', '').replace('-', ''))
    else:
        index = node.index('-')+1
        return int(node[index:])

def build_node_from_node_str(node):
    kind = None 
    if node.replace('-', '').isnumeric():
        kind = 'leaf'
    elif 'maxi' in node:
        kind = 'maxi'
    elif 'mini' in node:
        kind = 'mini'
    id = get_id_from_node_str(node)
    index = node.index('-')
    value = int(node[:index]) if node[:index].isnumeric() else None
    u = Node(id=id, kind=kind, value=value)
    return u

class Node():
    def __init__(self, id, value=None, kind='maxi'):
        self.id = id
        self.value = int(value) if value is not None else None
        self.kind = kind
        self.time = 0
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return self.children
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.id==other.id
    
    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.kind}-id:{self.id}-value:{self.value}-time:{self.time}"

def init(filename):
    
    '''
    * reads data from `filename` file
    * returns a dictionary of all `Node` objects
    '''

    with open(filename) as f:
        contents = f.read()
        contents = contents.splitlines()

        # split node to lists by level and add ids
        levels = dict()
        level_index = 0
        id = 1
        for line in contents:
            line_with_ids = copy.deepcopy(line)
            line_with_ids = line_with_ids.split(',')
            for i in range(len(line_with_ids)):
                family = line_with_ids[i].split(' ')
                for j in range(len(family)):
                    family[j] = family[j] + '-'+ str(id)
                    id += 1
                line_with_ids[i] = family
            levels[level_index] = line_with_ids
            level_index += 1
        
        # parse levels dict() and add Node objects to nodes dict()
        nodes = dict()
        root_str = levels[0][0][0]
        root = build_node_from_node_str(root_str)
        nodes[1] = root
        for level in levels:
            if level>0:
                for family in levels[level]:
                    parent_level = flatten_2d(levels[level-1])
                    parent_str = parent_level[levels[level].index(family)]
                    parent_id = get_id_from_node_str(parent_str)
                    for node in family:
                        u = build_node_from_node_str(node)
                        nodes[u.id] = u
                        nodes[parent_id].children.append(u)      
        return nodes

def minimax(nodes, AB=False):
    
    '''
    * executes the `minimax` algorithm with/without AB pruning depending on the corresponding flag
    * logs the nodes `visited`, their `values`, their `order` and the `non-visited` nodes
    '''

    print(f"I am minimax with{'out' if not AB else ''} AB pruning")
    time = 1

    def logs(nodes):
        
        '''
        * uses the `nodes` dictionary
        * logs the `output` messages
        '''
        unvisited = [node for node in nodes if nodes[node].time==0]
        visited = [nodes[node] for node in nodes if nodes[node].time!=0]
        visited.sort(key=lambda node:node.time)
        print(" * Root value:", res)
        print(" * Nodes visited counter:", time)
        print(" * Nodes visited:")
        i=1
        for node in visited[:-1]:
            print(f"\t u{node.id}: {node.value}->", end='\n' if i%5==0 else '')
            i += 1
        print(f"\t u{visited[len(visited)-1].id}: {visited[len(visited)-1].value}")
        print("  * Not visited nodes:")
        print(f"\t {unvisited}")

    def maxValue(node, mini_till_now):
        
        '''
        * the max-value method used by the `maximizing nodes`
        '''
        
        nonlocal AB
        nonlocal time
        node.time = time
        time += 1

        if node.kind == 'leaf':
            return node.value

        elif node.kind == 'mini':
            raise Exception("Called max-value method for mini node.")
        
        val = float('-inf')
        for child in node.children:
            mini = minValue(child, val)              
            val = max(val, mini)
            if AB and mini >= mini_till_now:
                return float('inf')
        node.value = val   
        return val

    def minValue(node, maxi_till_now):
                
        '''
        * the min-value method used by the `minimizing nodes`
        '''
        
        nonlocal AB
        nonlocal time
        node.time = time
        time += 1

        if node.kind == 'leaf':
            return node.value

        elif node.kind == 'maxi':
            raise Exception("Called min-value method for maxi node.")

        val = float('inf')
        for child in node.children:
            maxi = maxValue(child, val)
            val = min(val, maxi)
            if AB and maxi <= maxi_till_now:
                return float('-inf')
        node.value = val
        return val

    root = nodes[1]
    res = maxValue(root, float('inf'))

    logs(nodes)

def with_AB(nodes):

    '''
    * uses the `minimax` method to execute the algo using `AB pruning`
    '''
    
    minimax(nodes, True)

def without_AB(nodes):

    '''
    * uses the `minimax` method to execute the algo `without` using `AB pruning`
    '''
    
    minimax(nodes, False)


def main():

    '''
    * the main method
    * uses the previously declared methods and classes
    * reads the data from a txt file
    * solves with and without AB pruning
    '''
    
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 minimax.py input.txt")
    
    filename = sys.argv[1]

    nodes = init(filename)
    without_AB(nodes)
    
    nodes = init(filename)
    with_AB(nodes)
    

main()