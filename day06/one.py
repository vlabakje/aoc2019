import sys
from collections import defaultdict

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

def orbit_count(filename):
    orbits, roots = orbits_from(filename)
    def count(orbits, obj, c):
        for o in orbits[obj]:
            yield from count(orbits, o, c+1)
        yield c
    # figure out roots
    return sum(sum(count(orbits, root, 0)) for root in roots)

if __name__ == "__main__":
    print(orbit_count(sys.argv[1]))
