REL = {"R": (1, 0),
        "L": (-1, 0),
        "U": (0, 1),
        "D": (0, -1)}

def gen_coords(path):
    x, y = 0, 0
    for p in path:
        for i in range(int(p[1:])):
            x, y = x + REL[p[0]][0], y + REL[p[0]][1]
            yield x, y

def process_paths(filename):
    with open(filename) as fp:
        a, b, _ = fp.read().split("\n")
        a_coords = set(gen_coords(a.split(",")))
        b_coords = set(gen_coords(b.split(",")))
        matches = a_coords & b_coords
        short = 2 ** 32
        for m in matches:
            short = min(short, abs(m[0]) + abs(m[1]))
        return short

assert process_paths("example-135") == 135
assert process_paths("example-159") == 159
print(process_paths("input"))
