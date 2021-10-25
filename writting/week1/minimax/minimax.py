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
    
    def children_str(self):
        return [f"{child.kind}-{child.id}-{child.value}" for child in self.children]

    def __str__(self):
        return f"{self.kind}-id:{self.id}-value:{self.value}-time:{self.time}"

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

def minimax(nodes, AB=False):
    
    print(f"I am minimax with{'out' if not AB else ''} AB pruning")
    time = 1

    def logs(nodes):
        unvisited = [node for node in nodes if nodes[node].time==0]
        visited = [nodes[node] for node in nodes if nodes[node].time!=0]
        visited.sort(key=lambda node:node.time)
        print(" * Root value:", res)
        print(" * Nodes visited counter:", time)
        print(" * Nodes visited:")
        i=1
        for node in visited[:-1]:
            print(f"\t node {node.id}: {node.value} ->", end='\n' if i%5==0 else '')
            i += 1
        print(f"\t node {visited[len(visited)-1].id}: {visited[len(visited)-1].value}")
        print("  * Not visited nodes:")
        print(f"\t {unvisited}")

    def maxValue(node, mini_till_now):
        nonlocal AB
        nonlocal time
        node.time = time
        time += 1

        if node.kind == 'leaf':
            return node.value

        elif node.kind == 'mini':
            raise Exception("Called max-value function for mini node.")
        
        val = float('-inf')
        for child in node.children:
            mini = minValue(child, val)              
            val = max(val, mini)
            if AB and mini >= mini_till_now:
                return float('inf')
        node.value = val   
        return val

    def minValue(node, maxi_till_now):
        nonlocal AB
        nonlocal time
        node.time = time
        time += 1

        if node.kind == 'leaf':
            return node.value

        elif node.kind == 'maxi':
            raise Exception("Called min-value function for maxi node.")

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
    minimax(nodes, True)
    assert nodes[1].value == 5     and nodes[1].time == 1
    assert nodes[2].value == 3     and nodes[2].time == 2
    assert nodes[3].value == None  and nodes[3].time == 15
    assert nodes[4].value == 5     and nodes[4].time == 21
    assert nodes[5].value == 3     and nodes[5].time == 3 
    assert nodes[6].value == None  and nodes[6].time == 9
    assert nodes[7].value == 1     and nodes[7].time == 16
    assert nodes[8].value == None  and nodes[8].time == 0
    assert nodes[9].value == 5     and nodes[9].time == 22
    assert nodes[10].value == None and nodes[10].time == 30
    assert nodes[11].value == 3    and nodes[11].time == 4 
    assert nodes[12].value == None and nodes[12].time == 7
    assert nodes[13].value == 1    and nodes[13].time == 10
    assert nodes[14].value == 7    and nodes[14].time == 13
    assert nodes[15].value == None and nodes[15].time == 0
    assert nodes[16].value == 1    and nodes[16].time == 17
    assert nodes[17].value == None and nodes[17].time == 0
    assert nodes[18].value == 0    and nodes[18].time == 23
    assert nodes[19].value == 5    and nodes[19].time == 27
    assert nodes[20].value == 7    and nodes[20].time == 31
    assert nodes[21].value == None and nodes[21].time == 0
    assert nodes[22].value == None and nodes[22].time == 0
    assert nodes[23].value == 4    and nodes[23].time == 5
    assert nodes[24].value == 3    and nodes[24].time == 6
    assert nodes[25].value == 3    and nodes[25].time == 8
    assert nodes[26].value == 4    and nodes[26].time == 0
    assert nodes[27].value == 1    and nodes[27].time == 0
    assert nodes[28].value == 1    and nodes[28].time == 11
    assert nodes[29].value == 2    and nodes[29].time == 12
    assert nodes[30].value == 7    and nodes[30].time == 14
    assert nodes[32].value == 2    and nodes[32].time == 0
    assert nodes[31].value == 1    and nodes[31].time == 0
    assert nodes[33].value == 1    and nodes[33].time == 18
    assert nodes[34].value == 7    and nodes[34].time == 19
    assert nodes[35].value == 5    and nodes[35].time == 20
    assert nodes[36].value == 2    and nodes[36].time == 0
    assert nodes[37].value == 4    and nodes[37].time == 0
    assert nodes[38].value == 8    and nodes[38].time == 24
    assert nodes[39].value == 0    and nodes[39].time == 25
    assert nodes[40].value == 3    and nodes[40].time == 26
    assert nodes[41].value == 6    and nodes[41].time == 28
    assert nodes[42].value == 5    and nodes[42].time == 29
    assert nodes[43].value == 7    and nodes[43].time == 32
    assert nodes[44].value == 9    and nodes[44].time == 33
    assert nodes[45].value == 2    and nodes[45].time == 0
    assert nodes[46].value == 5    and nodes[46].time == 0
    assert nodes[47].value == 3    and nodes[47].time == 0
    assert nodes[48].value == 1    and nodes[48].time == 0
    assert nodes[49].value == 8    and nodes[49].time == 0

def without_AB(nodes):
    minimax(nodes, False)
    assert nodes[1].value == 5   and nodes[1].time == 1
    assert nodes[2].value == 3   and nodes[2].time == 2
    assert nodes[3].value == 1   and nodes[3].time == 20
    assert nodes[4].value == 5   and nodes[4].time == 30
    assert nodes[5].value == 3   and nodes[5].time == 3 
    assert nodes[6].value == 7   and nodes[6].time == 11
    assert nodes[7].value == 1   and nodes[7].time == 21
    assert nodes[8].value == 2   and nodes[8].time == 26
    assert nodes[9].value == 5   and nodes[9].time == 31
    assert nodes[10].value == 7  and nodes[10].time == 39
    assert nodes[11].value == 3  and nodes[11].time == 4 
    assert nodes[12].value == 1  and nodes[12].time == 7
    assert nodes[13].value == 1  and nodes[13].time == 12
    assert nodes[14].value == 7  and nodes[14].time == 15
    assert nodes[15].value == 1  and nodes[15].time == 17
    assert nodes[16].value == 1  and nodes[16].time == 22
    assert nodes[17].value == 2  and nodes[17].time == 27
    assert nodes[18].value == 0  and nodes[18].time == 32
    assert nodes[19].value == 5  and nodes[19].time == 36
    assert nodes[20].value == 7  and nodes[20].time == 40
    assert nodes[21].value == 2  and nodes[21].time == 43
    assert nodes[22].value == 1  and nodes[22].time == 46
    assert nodes[23].value == 4  and nodes[23].time == 5
    assert nodes[24].value == 3  and nodes[24].time == 6
    assert nodes[25].value == 3  and nodes[25].time == 8
    assert nodes[26].value == 4  and nodes[26].time == 9
    assert nodes[27].value == 1  and nodes[27].time == 10
    assert nodes[28].value == 1  and nodes[28].time == 13
    assert nodes[29].value == 2  and nodes[29].time == 14
    assert nodes[30].value == 7  and nodes[30].time == 16
    assert nodes[31].value == 1  and nodes[31].time == 18
    assert nodes[32].value == 2  and nodes[32].time == 19
    assert nodes[33].value == 1  and nodes[33].time == 23
    assert nodes[34].value == 7  and nodes[34].time == 24
    assert nodes[35].value == 5  and nodes[35].time == 25
    assert nodes[36].value == 2  and nodes[36].time == 28
    assert nodes[37].value == 4  and nodes[37].time == 29
    assert nodes[38].value == 8  and nodes[38].time == 33
    assert nodes[39].value == 0  and nodes[39].time == 34
    assert nodes[40].value == 3  and nodes[40].time == 35
    assert nodes[41].value == 6  and nodes[41].time == 37
    assert nodes[42].value == 5  and nodes[42].time == 38
    assert nodes[43].value == 7  and nodes[43].time == 41
    assert nodes[44].value == 9  and nodes[44].time == 42
    assert nodes[45].value == 2  and nodes[45].time == 44
    assert nodes[46].value == 5  and nodes[46].time == 45
    assert nodes[47].value == 3  and nodes[47].time == 47
    assert nodes[48].value == 1  and nodes[48].time == 48
    assert nodes[49].value == 8  and nodes[49].time == 49


def main():

    if len(sys.argv) != 2:
        sys.exit("Usage: python3 minimax.py input.txt")
    
    filename = sys.argv[1]

    nodes = init(filename)
    without_AB(nodes)
    
    nodes = init(filename)
    with_AB(nodes)
    

main()