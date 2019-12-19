import argparse

from pysat import solvers
from numpy.random.mtrand import RandomState

from output import *
from predictor import *
from predictor.predictor import Predictor
from predictor.verifier import Verifier
from predictor.instance.models.var import Backdoor

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('instance', type=str, help='instance of problem')
parser.add_argument('backdoors', type=str, help='load backdoor from specified file')
parser.add_argument('-i', '--incremental', action='store_true', help='incremental mode')
parser.add_argument('-r', '--repeats', metavar='1', type=int, default=1, help='repeats count')
parser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')

args = parser.parse_args()

inst = instance.get(args.instance)
assert inst.check()

backdoors = Backdoor.load(args.backdoors)
solver = solvers.Glucose4

cell = Cell(
    path=['output', '_verify_logs', inst.tag],
    logger=tools.logger(),
    debugger=tools.debugger(verb=args.verbosity)
).open(description=args.description)


def iteration(i, f, backdoor, *args):
    cell.log('Iteration: %d' % i, '------------------------------------------------------')
    count = args[0] if len(args) > 0 else 2 ** len(backdoor)
    cell.log('Run verify for backdoor: %s' % backdoor, 'With %d cases:' % count)
    value = f(backdoor, *args)
    cell.log('End verifier with value: %.7g' % value)
    cell.log('------------------------------------------------------')
    return value


rs = RandomState()
predictor = Predictor(
    rs=rs,
    output=cell,
    instance=inst,
    method=method.GuessAndDetermine(
        chunk_size=1000,
        concurrency=concurrency.pysat.MapPool(
            incremental=False,
            threads=args.threads,
            solver=solver,
            propagator=solver,
        )
    )
)

empty = Backdoor.empty()
cell.touch().log('\n'.join('-- ' + s for s in str(predictor).split('\n')))
cell.log('------------------------------------------------------')
full = iteration(0, predictor.predict, empty, args.repeats)
print('Full: %.7g s' % full)

verifier = Verifier(
    output=cell,
    instance=inst,
    chunk_size=1024,
    concurrency=concurrency.pysat.MapPool(
        keep=True,
        threads=args.threads,
        incremental=args.incremental,
        solver=solver,
        propagator=solver,
    )
)


def process(backdoor: Backdoor):
    values = []
    cell.touch().log('\n'.join('-- ' + s for s in str(verifier).split('\n')))
    cell.log('------------------------------------------------------')
    for i in range(args.repeats):
        value = iteration(i, verifier.verify, backdoor)
        values.append(value)
        if args.incremental:
            verifier.concurrency.terminate()

    cell.log('------------------------------------------------------')
    cell.log('Summary: %.7g' % (sum(values) / len(values)))
    return values


for bd in backdoors:
    summary = process(bd)
    summary = sum(summary) / len(summary)
    rate = summary / full
    cell.log('Rate: %.4g' % rate)
    print('Rate %.4g with backdoor: %s' % (rate, bd))

cell.close()
