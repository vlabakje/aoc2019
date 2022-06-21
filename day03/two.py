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

def match_distances(coords, matches):
    output = {}
    for i, c in enumerate(coords):
        if c in matches:
            if c not in output:
                output[c] = i + 1
    return output

def process_paths(filename):
    with open(filename) as fp:
        a, b, _ = fp.read().split("\n")
        a_coords = list(gen_coords(a.split(",")))
        b_coords = list(gen_coords(b.split(",")))
        matches = set(a_coords) & set(b_coords)
        a_dist = match_distances(a_coords, matches)
        b_dist = match_distances(b_coords, matches)
        lowest = 2**32
        for m in matches:
            # print(f"{m=} {a_dist[m]=} {b_dist[m]=} {a_dist[m] + b_dist[m]}")
            lowest = min(lowest, a_dist[m] + b_dist[m])
        return lowest

assert process_paths("example-135") == 410
assert process_paths("example-159") == 610
print(process_paths("input"))
