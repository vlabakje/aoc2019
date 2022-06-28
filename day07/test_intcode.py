import intcode

def test_add_multiply():
    assert intcode.from_str("1,0,0,3,99").run() == 1
    assert intcode.from_str("1,9,10,3,2,3,11,0,99,30,40,50").run() == 3500
    assert intcode.from_str("1,1,1,4,99,5,6,0,99").run() == 30


def test_modes():
    assert intcode.from_str("1002,4,3,4,33").run() == 1002


def io(code, inputs, expected):
     ic = intcode.from_str(code)
     ic.input = inputs
     ic.output = []
     ic.run()
     return ic.output == expected

def test_io():
    # position mode, equal
    assert io("3,9,8,9,10,9,4,9,99,-1,8", [8], [1])
    assert io("3,9,8,9,10,9,4,9,99,-1,8", [7], [0])
    # immediate mode, less than
    assert io("3,3,1107,-1,8,3,4,3,99", [9], [0])
    assert io("3,3,1107,-1,8,3,4,3,99", [1], [1])
    # with jumps
    assert io("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [9], [1])
    assert io("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0], [0])
