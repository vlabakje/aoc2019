import t_intcode
import itertools
import queue
import sys
import threading

class Amplifier(threading.Thread):
    def __init__(self, code, phase, q_in, q_out):
        self.ic = t_intcode.IntCode(code, input_=q_in.get, output=q_out.put, name=f"[{phase}]")
        super().__init__(target=self.ic.run)
        q_in.put(phase)
    

def run_amplifiers(code, phases):
    queues = [queue.Queue(maxsize=1) for _ in range(len(phases))]
    amps = [Amplifier(code[:], phase, queues[i], queues[(i+1)%5]) for i, phase in enumerate(phases)]
    any(amp.start() for amp in amps)
    queues[0].put(0)
    any(amp.join() for amp in amps)
    assert queues[0].qsize() == 1 and all(q.qsize() == 0 for q in queues[1:])
    return queues[0].get()


def find_max_thruster(code, phases):
    top, best = 0, None
    for seq in itertools.permutations(phases):
        res = run_amplifiers(code, seq)
        if res > top:
            top, best = res, seq
    return top, best

if __name__ == "__main__":
    print(find_max_thruster(t_intcode.from_file(sys.argv[1]).code, [9, 8, 7, 6, 5]))
