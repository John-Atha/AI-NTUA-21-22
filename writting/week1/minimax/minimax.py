import sys
import copy

def flatten(l):
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
    value = int(node) if node.isnumeric() else None
    u = Node(id=id, kind=kind, value=value)
    return u

class Node():
    def __init__(self, id, value=None, kind='maxi'):
        self.id = id
        self.value = float(value) if value else None
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
    
    def children_str(self):
        return [f"{child.kind}-{child.id}-{child.value}" for child in self.children]

    def __str__(self):
        return f"{self.kind}-{self.id}-{self.value}-{self.children_str()}"

def init(filename):

    with open(filename) as f:
        contents = f.read()
        contents = contents.splitlines()
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
        # print(levels)
        # print('----------------------------')
        
        nodes = dict()
        root_str = levels[0][0][0]
        # print(root_str)
        root = build_node_from_node_str(root_str)
        nodes[1] = root
        for level in levels:
            if level>0:
                # print(levels[level])
                for family in levels[level]:
                    parent_level = flatten(levels[level-1])
                    parent_str = parent_level[levels[level].index(family)]
                    # print(parent_level)
                    # print(family, 'from: ', parent_str)
                    parent_id = get_id_from_node_str(parent_str)
                    for node in family:
                        u = build_node_from_node_str(node)
                        nodes[u.id] = u
                        nodes[parent_id].children.append(u)      
        return nodes

def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python3 minimax.py input.txt")
    
    filename = sys.argv[1]
    
    nodes = init(filename)
    
    for node in nodes:
        print(node, ':', nodes[node])


main()