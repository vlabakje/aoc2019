import sys
from typing import List

def read_program(filename: str) -> List[int]:
    with open(filename) as fp:
        return list(map(int, fp.read().strip().split(",")))

def parse_operation(opcode: int):
    params, opcode = divmod(opcode, 100)
    params, p1m = divmod(params, 10)
    p3m, p2m = divmod(params, 10)
    return opcode, (p1m, p2m, p3m)

def intcode_get(intcode, address, mode):
    if mode == 1:
        return intcode[address]
    if mode == 0:
        return intcode[intcode[address]]
    raise NotImplementedError(f"invalid mode {address=} {mode=} (0, 1 supported)")

def intcode_set(intcode, address, mode, value):
    if mode != 0:
        raise NotImplementedError(f"invalid mode {address=} {mode=}")
    intcode[intcode[address]] = value

def op_three(intcode, ip, params, f) -> int:
    intcode_set(intcode, ip + 3, params[2], f(
            intcode_get(intcode, ip + 1, params[0]),
            intcode_get(intcode, ip + 2, params[1])))
    return 4

def op_input(intcode, ip):
    value = int(input("-> "))
    intcode_set(intcode, ip + 1, 0, value)
    return 2

def op_output(intcode, ip):
    print("out " + str(intcode_get(intcode, ip + 1, 0)))
    return 2

def op_jump_if(intcode, ip, params, value):
    p1 = intcode_get(intcode, ip + 1, params[0])
    if (value and p1) or (not value and p1 == 0):
        return intcode_get(intcode, ip + 2, params[1])
    return ip + 3

def run(intcode: List[int]):
    ip = 0
    while intcode[ip] != 99:  # halt
        opcode, params = parse_operation(intcode[ip])
        print(",".join(str(i) for i in intcode), f"{ip=}")
        if opcode == 1:  # addition
            ip += op_three(intcode, ip, params, lambda x, y: x + y)
        elif opcode == 2:  # multiplication
            ip += op_three(intcode, ip, params, lambda x, y: x * y)
        elif opcode == 3:  # input
            ip += op_input(intcode, ip)
        elif opcode == 4:  # output
            ip += op_output(intcode, ip)
        elif opcode == 5:  # jump if true
            ip = op_jump_if(intcode, ip, params, True)
        elif opcode == 6:  # jump if false
            ip = op_jump_if(intcode, ip, params, False)
        elif opcode == 7:  # less then
            ip += op_three(intcode, ip, params, lambda x, y: 1 if x < y else 0)
        elif opcode == 8:  # equals
            ip += op_three(intcode, ip, params, lambda x, y: 1 if x == y else 0)
        else:
            raise NotImplementedError(f"unknown opcode {ip=} {intcode[ip]=} {opcode=} {params=}")
        print(",".join(str(i) for i in intcode), f"{ip=}")
        print("---")
    return intcode[0]

if __name__ == "__main__":
    run(read_program(sys.argv[1]))
