import sys
from typing import List

def read_program(filename: str) -> List[int]:
    with open(filename) as fp:
        return list(map(int, fp.read().strip().split(",")))

def run(intcode: List[int]):
    pc = 0
    while intcode[pc] != 99:  # halt
        #print(",".join(str(i) for i in intcode), f"{pc=}")
        if intcode[pc] == 1:  # addition
            intcode[intcode[pc + 3]] = intcode[intcode[pc + 1]] + intcode[intcode[pc + 2]]
            pc += 4
        elif intcode[pc] == 2:  # multiplication
            intcode[intcode[pc + 3]] = intcode[intcode[pc + 1]] * intcode[intcode[pc + 2]]
            pc += 4
        else:
            raise NotImplementedError(f"unknown opcode {intcode[pc]}")
        #print(",".join(str(i) for i in intcode), f"{pc=}")
        #print("---")
    return intcode[0]

def main(intcode):
    for noun in range(100):
        for verb in range(100):
            ic = intcode[:]
            ic[1] = noun
            ic[2] = verb
            result = run(ic)
            # print(f"{noun=} {verb=} {result=}")
            if result == 19690720:
                return 100 * noun + verb

if __name__ == "__main__":
    print(main(read_program(sys.argv[1])))
