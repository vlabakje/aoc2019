from collections import Counter
import sys

def layers(filename, wide, tall):
    with open(filename) as fp:
        data = fp.read().strip()
        assert len(data) % (wide*tall) == 0, "incomplete frame at the end of data"
        for i in range(0, len(data), wide * tall):
            yield data[i:i+(wide*tall)]

def render(filename, wide, tall):
    layers_ = list(layer for layer in layers(filename, wide, tall))
    def pixel(x, y):
        for layer in layers_:
            if layer[wide*y+x] != '2':
                if layer[wide*y+x] == "0":
                    return " "
                return layer[wide*y+x]
    image = [[None] * wide for i in range(tall)]
    for y in range(tall):
        for x in range(wide):
            image[y][x] = pixel(x, y)
    for i in image:
         print("".join(i))

if __name__ == "__main__":
    render("input", 25, 6)
