import argparse

from pysat import solvers as slvs
from numpy.random.mtrand import RandomState

from output import *
from method import *
from method.instance.models.var import Backdoor

solvers = {
    'cd': slvs.Cadical,
    'g3': slvs.Glucose3,
    'g4': slvs.Glucose4,
    'lgl': slvs.Lingeling,
    'mcb': slvs.MapleChrono,
    'mcm': slvs.MapleCM,
    'mpl': slvs.Maplesat,
    'mc': slvs.Minicard,
    'm22': slvs.Minisat22,
    'mgh': slvs.MinisatGH,
}

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('instance', type=str, help='instance of problem')
parser.add_argument('backdoors', type=str, help='load backdoor from specified file')
parser.add_argument('-i', '--incremental', action='store_true', help='incremental mode')
parser.add_argument('-r', '--repeats', metavar='1', type=int, default=1, help='repeats count')
parser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')
parser.add_argument('-dall', '--debug_all', action='store_true', help='debug on all nodes')

parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
parser.add_argument('-pr', '--propagator', metavar='str', type=str, default='', help='SAT-solver to propagate')

args, _ = parser.parse_known_args()

inst = instance.get(args.instance)
assert inst.check()

solver = solvers[args.solver]
propagator = solvers[args.propagator] if args.propagator else solver

backdoors = Backdoor.load(args.backdoors)

cell = Cell(
    path=['output', '_verify_logs', inst.tag],
    largs={},
    dargs={
        'dall': args.debug_all,
        'verb': args.verbosity
    },
).open(description=args.description)


def iteration(i, method, backdoor, *args, **kwargs):
    cell.log('Iteration: %d' % i, '------------------------------------------------------')
    estimation = method.estimate(backdoor, *args, **kwargs)
    cell.log('------------------------------------------------------')
    return estimation.value


rs = RandomState()
monte_carlo = MonteCarlo(
    rs=rs,
    output=cell,
    instance=inst,
    function=function.GuessAndDetermine(
        chunk_size=1000,
    ),
    concurrency=concurrency.pysat.MapPool(
        solver=solver,
        propagator=propagator,
        incremental=False,
        threads=args.threads,
        measure=concurrency.measure.Propagations(),
    )
)

empty = Backdoor.empty()
cell.touch().log('\n'.join('-- ' + s for s in str(monte_carlo).split('\n')))
cell.log('------------------------------------------------------')
full = iteration(0, monte_carlo, empty, count=args.repeats)
# full = 10000.0
print('Full: %.7g s' % full)

verification = Verification(
    rs=rs,
    output=cell,
    instance=inst,
    can_cache=False,
    chunk_size=1024,
    concurrency=concurrency.pysat.MapPool(
        keep=True,
        solver=solver,
        propagator=propagator,
        threads=args.threads,
        incremental=args.incremental,
        measure=concurrency.measure.Propagations(),
    )
)


def process(backdoor: Backdoor):
    values = []
    cell.touch().log('\n'.join('-- ' + s for s in str(verification).split('\n')))
    cell.log('------------------------------------------------------')
    for i in range(args.repeats):
        value = iteration(i, verification, backdoor)
        values.append(value)
        if args.incremental:
            verification.concurrency.terminate()

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
