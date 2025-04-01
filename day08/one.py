from collections import Counter
import sys

def layers(filename, wide, tall):
    with open(filename) as fp:
        data = fp.read().strip()
        assert len(data) % (wide*tall) == 0, "incomplete frame at the end of data"
        for i in range(0, len(data), wide * tall):
            yield data[i:i+(wide*tall)]


def fewest_zeros(layer_list):
    counters = {}
    fewest, fewest_index = None, None
    for i, layer in enumerate(layer_list):
        counters[i] = Counter(layer)
        if fewest is None or counters[i]["0"] < fewest:
            fewest, fewest_index = counters[i]["0"], i
    ones, twos = counters[fewest_index]["1"], counters[fewest_index]["2"]
    print(ones * twos)



if __name__ == "__main__":
    #for i, layer in enumerate(layers("test", 3, 2)):
    #    print(f"Layer {i}: {layer}")
    #for i, layer in enumerate(layers("input", 25, 6)):
    #    print(f"Layer {i}: {layer}")
    fewest_zeros(layers("input", 25, 6))
