import intcode
import itertools
import sys

def run_amplifiers(code, seq):
    amp_in = 0
    for i in seq:
        ic = intcode.IntCode(code[:], [i, amp_in], output=[])
        ic.run()
        amp_in = ic.output[0]
    return amp_in
    

def find_max_thruster(code):
    top, best = 0, None
    for seq in itertools.permutations(range(5)):
        res = run_amplifiers(code, seq)
        if res > top:
            top, best = res, seq
    return top, best

def main(filename):
    code = intcode.from_file(filename).code
    print(find_max_thruster(code))

if __name__ == "__main__":
    main(sys.argv[1])
