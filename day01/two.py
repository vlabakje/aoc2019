import sys

def masses(filename):
    with open(filename) as fp:
        for line in fp:
            if line:
                yield int(line)

def fuel_requirements(masses):
    for mass in masses:
        m = max(0, mass // 3 - 2)
        while m > 0:
            yield m
            m = m // 3 - 2

def main(filename):
    print(sum(fuel_requirements(masses(filename))))


if __name__ == "__main__":
    assert sum(fuel_requirements((12, ))) == 2
    assert sum(fuel_requirements((100756, ))) == 50346
    main(sys.argv[1])
