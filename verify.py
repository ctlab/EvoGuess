import argparse
from pysat import solvers

from output import *
from predictor import *
from predictor.verifier import Verifier
from predictor.instance.models.var import Backdoor

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('instance', type=str, help='instance of problem')
parser.add_argument('-r', '--repeats', metavar='1', type=int, default=1, help='repeats count')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')

args = parser.parse_args()

inst = instance.get(args.instance)
assert inst.check()

cell = Cell(
    path=['output', '_verify_logs', 'test', inst.tag],
    logger=tools.logger(),
    debugger=tools.debugger(verb=args.verbosity)
).open(description=args.description)

pool = concurrency.SinglePool(
    threads=4,
    solver=solver.RoKK(interrupter=solver.interrupter.Base(tl=0)),
    propagator=solver.RoKK(interrupter=solver.interrupter.Base(tl=0)),
)

times = []
bd = Backdoor([2, 6, 7, 12, 18, 26, 34, 35, 41, 42])
for i in range(10):
    cell.touch()
    verifier = Verifier(
        keep=True,
        output=cell,
        chunk_size=1000,
        concurrency=pool
    )
    times.append([
        verifier.verify(inst, Backdoor.empty()),
        verifier.verify(inst, bd)
    ])
    rate = times[-1][0] / times[-1][1]
    cell.log('Rate %.2g with backdoor: %s' % (rate, bd))

cell.close()

full = sum([time[0] for time in times]) / len(times)
summary = sum([time[1] for time in times]) / len(times)
print('Times: full %.7g s, summary %.7g s' % (full, summary))

rate = full / summary
print('Rate %.2g with backdoor: %s' % (rate, bd))
