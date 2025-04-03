from collections.abc import Callable
import sys

Params = tuple[int, int, int]

def read_program(filename: str) -> list[int]:
    with open(filename) as fp:
        return list(map(int, fp.read().strip().split(",")))

def parse_operation(opcode: int):
    params, opcode = divmod(opcode, 100)
    params, p1m = divmod(params, 10)
    p3m, p2m = divmod(params, 10)
    return opcode, (p1m, p2m, p3m)

class Intcode:
    ip = 0
    relative_base = 0

    def __init__(self, intcode: list[int], inputs: list[int]):
        self.mem = intcode
        self.inputs = inputs

    def resolve(self, address: int, mode: int) -> int:
        if mode == 0:  # position mode
            return self.get(address, 1)
        elif mode == 2:  # relative base mode
            return self.get(address, 1) + self.relative_base
        elif mode == 1:  # immediate mode
            return address
        raise NotImplementedError(f"invalid mode {address=} {mode=}")

    def set(self, address: int, mode: int, value: int) -> None:
        address = self.resolve(address, mode)
        # print(f"write {value=} {address=} {len(self.mem)=}")
        if len(self.mem) <= address:
            self.mem.extend(0 for _ in range(address - len(self.mem)+1))
        self.mem[address] = value
        
    def get(self, address: int, mode: int) -> int:
        address = self.resolve(address, mode)
        if len(self.mem) < address:
            self.mem.extend(0 for _ in range(address - len(self.mem)+1))
        return self.mem[address]

    def op_three(self, params: Params, f: Callable[[int, int], int]) -> int:
        self.set(self.ip + 3, params[2], f(
                self.get(self.ip + 1, params[0]),
                self.get(self.ip + 2, params[1])))
        return self.ip + 4

    def op_input(self, params: Params) -> int:
        self.set(self.ip + 1, params[0], self.inputs.pop(0))
        return self.ip + 2

    def op_output(self, params: Params) -> int:
        print("out " + str(self.get(self.ip + 1, params[0])))
        return self.ip + 2

    def op_jump_if(self, params: Params, value: bool) -> int:
        p1 = self.get(self.ip + 1, params[0])
        if (value and p1) or (not value and p1 == 0):
            return self.get(self.ip + 2, params[1])
        return self.ip + 3

    def run(self) -> int:
        while self.mem[self.ip] != 99:  # halt
            opcode, params = parse_operation(self.mem[self.ip])
            # print(f"ip={self.ip} {opcode=} rb={self.relative_base} ", ",".join(str(i) for i in self.mem)[:70])
            if opcode == 1:  # addition
                self.ip = self.op_three(params, lambda x, y: x + y)
            elif opcode == 2:  # multiplication
                self.ip = self.op_three(params, lambda x, y: x * y)
            elif opcode == 3:  # input
                self.ip = self.op_input(params)
            elif opcode == 4:  # output
                self.ip = self.op_output(params)
            elif opcode == 5:  # jump if true
                self.ip = self.op_jump_if(params, True)
            elif opcode == 6:  # jump if false
                self.ip = self.op_jump_if(params, False)
            elif opcode == 7:  # less then
                self.ip = self.op_three(params, lambda x, y: 1 if x < y else 0)
            elif opcode == 8:  # equals
                self.ip = self.op_three(params, lambda x, y: 1 if x == y else 0)
            elif opcode == 9:  # relative base offset
                self.relative_base += self.get(self.ip+1, params[0])
                self.ip += 2
            else:
                raise NotImplementedError(f"unknown opcode {self.ip=} {self.mem[self.ip]=} {opcode=} {params=}")
        return self.mem[0]

if __name__ == "__main__":
    ic = Intcode(read_program(sys.argv[1]), list(map(int, sys.argv[2:])))
    ic.run()
