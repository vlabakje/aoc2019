import asyncio
import intcode
import itertools
import queue
import sys
import threading

class Amplifier():
    def __init__(self, code, phase, q_in, q_out):
        self.ic = intcode.IntCode(code, input_=q_in.get, output=q_out.put, name=f"[{phase}]")
        q_in.put_nowait(phase)

    async def run(self):
        await self.ic.run()
    

async def run_amplifiers(code, phases):
    queues = [asyncio.Queue() for _ in range(len(phases))]
    amps = [Amplifier(code[:], phase, queues[i], queues[(i+1)%5]) for i, phase in enumerate(phases)]
    tasks = []
    for amp in amps:
        tasks.append(asyncio.create_task(amp.run()))
    await queues[0].put(0)
    await asyncio.gather(*tasks)
    assert queues[0].qsize() == 1 and all(q.qsize() == 0 for q in queues[1:])
    return await queues[0].get()


async def find_max_thruster(code, phases):
    top, best = 0, None
    for seq in itertools.permutations(phases):
        res = await run_amplifiers(code, seq)
        if res > top:
            top, best = res, seq
    return top, best

if __name__ == "__main__":
    print(asyncio.run(find_max_thruster(intcode.from_file(sys.argv[1]).code, [9, 8, 7, 6, 5])))
