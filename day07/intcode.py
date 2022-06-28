from typing import List

class IntCode:
    def __init__(self, code, input_=[], output=None, name=None):
        self.code = code
        self.input = input_
        self.output = output
        self.ip = 0
        self.name = name

    def get(self, address, mode):
        if mode == 1:
            return self.code[address]
        if mode == 0:
            return self.code[self.code[address]]
        raise NotImplementedError(f"invalid mode {address=} {mode=} (0, 1 supported)")

    def set(self, address, mode, value):
        if mode != 0:
            raise NotImplementedError(f"invalid mode {address=} {mode=}")
        self.code[self.code[address]] = value

    def op_three(self, params, f) -> int:
        self.set(self.ip + 3, params[2], f(
                self.get(self.ip + 1, params[0]),
                self.get(self.ip + 2, params[1])))
        self.ip += 4

    def op_input(self):
        if isinstance(self.input, list):
            self.set(self.ip + 1, 0, self.input.pop(0))
        elif callable(self.input):
            self.set(self.ip + 1, 0, self.input())
        else:
            raise RuntimeError(f"unable to handle input type {type(self.input)=}")
        self.debug(f"input: {self.get(self.ip + 1, 0)}")
        self.ip += + 2

    def op_output(self):
        if isinstance(self.output, list):
            self.output.append(self.get(self.ip + 1, 0))
        elif callable(self.output):
            self.output(self.get(self.ip + 1, 0))
        else:
            raise RuntimeError(f"unable to handle output type {type(self.output)=}")
        self.ip += 2

    def op_jump_if(self, params, value):
        p1 = self.get(self.ip + 1, params[0])
        if (value and p1) or (not value and p1 == 0):
            self.ip = self.get(self.ip + 2, params[1])
        else:
            self.ip += 3

    def run(self):
        while self.code[self.ip] != 99:  # halt
            opcode, params = parse_operation(self.code[self.ip])
            self.debug(",".join(str(i) for i in self.code)[:70])
            if opcode == 1:  # addition
                self.op_three(params, lambda x, y: x + y)
            elif opcode == 2:  # multiplication
                self.op_three(params, lambda x, y: x * y)
            elif opcode == 3:  # input
                self.op_input()
            elif opcode == 4:  # output
                self.op_output()
            elif opcode == 5:  # jump if true
                self.op_jump_if(params, True)
            elif opcode == 6:  # jump if false
                self.op_jump_if(params, False)
            elif opcode == 7:  # less then
                self.op_three(params, lambda x, y: 1 if x < y else 0)
            elif opcode == 8:  # equals
                self.op_three(params, lambda x, y: 1 if x == y else 0)
            else:
                raise NotImplementedError(f"unknown opcode {self.ip=} {self.code[self.ip]=} {opcode=} {params=}")
            self.debug(",".join(str(i) for i in self.code)[:70])
            self.debug("---")
        return self.code[0]

    def debug(self, msg):
        if self.name:
            print(f"{self.name} {self.ip=} {msg}")
        else:
            print(msg)

def parse_operation(opcode: int):
    params, opcode = divmod(opcode, 100)
    params, p1m = divmod(params, 10)
    p3m, p2m = divmod(params, 10)
    return opcode, (p1m, p2m, p3m)

def from_file(filename: str) -> IntCode:
    with open(filename) as fp:
        return IntCode(list(map(int, fp.read().strip().split(","))))

def from_str(code: str) -> IntCode:
    return IntCode(list(map(int, code.split(","))))
