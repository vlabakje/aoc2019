import sys
from collections import defaultdict

class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []

def orbits_from(filename):
    orbits = defaultdict(list)
    objects = set()
    orbiters = set()
    with open(filename) as fp:
        for line in fp:
            parts = line.strip().split(")")
            if len(parts) == 2:
                orbits[parts[0]].append(parts[1])
                objects.add(parts[0])
                orbiters.add(parts[1])
    return orbits, objects - orbiters

def build_tree(filename):
    orbits, roots = orbits_from(filename)
    assert len(roots) == 1
    root = list(roots)[0]
    nodes = {root: Node(root, None)} 
    def populate(orbits, nodes, current):
        for satellite in orbits[current]:
            nodes[satellite] = Node(satellite, nodes[current])
            nodes[current].children.append(nodes[satellite])
            populate(orbits, nodes, satellite)
    populate(orbits, nodes, root)
    return path_between_length(nodes, 'YOU', 'SAN')


def path_between_length(nodes, a, b):
    def root_path(nodes, name):
        path = []
        node = nodes[name]
        while node.parent:
            node = node.parent
            path.append(node.name)
        return path
    a_path = root_path(nodes, a)
    b_path = root_path(nodes, b)
    for i, node in enumerate(a_path):
        if node in b_path:
            return i + b_path.index(node)


if __name__ == "__main__":
    print(build_tree(sys.argv[1]))
