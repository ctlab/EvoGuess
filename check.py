import argparse

from numpy.random.mtrand import RandomState
from pysat import solvers as slvs

from output import *
from predictor import *
from predictor.instance.models.var import Backdoor

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
parser.add_argument('function', type=str, help='estimation function')
parser.add_argument('backdoors', type=str, help='load backdoor from specified file')
parser.add_argument('-i', '--incremental', action='store_true', help='incremental mode')
parser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')
parser.add_argument('-dall', '--debug_all', action='store_true', help='debug on all nodes')

parser.add_argument('-tl', metavar='5', type=int, default=5, help='time limit for ibs')
parser.add_argument('-n', '--sampling', metavar='1000', type=int, default=1000, help='estimation sampling')
parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
parser.add_argument('-pr', '--propagator', metavar='str', type=str, default='', help='SAT-solver to propagate')

args = parser.parse_args()

inst = instance.get(args.instance)
assert inst.check(), "Cnf is missing"

Function = function.get(args.function)
solver = solvers[args.solver]
propagator = solvers[args.propagator] if args.propagator else solver

backdoors = Backdoor.load(args.backdoors)

cell = Cell(
    path=['output', '_check_logs', inst.tag],
    largs={},
    dargs={
        'dall': args.debug_all,
        'verb': args.verbosity
    },
).open(description=args.description)

rs = RandomState()
monte_carlo = MonteCarlo(
    rs=rs,
    output=cell,
    instance=inst,
    function=Function(
        time_limit=args.tl,
        chunk_size=10000,
        concurrency=concurrency.pysat.PebbleMap(
            threads=args.threads,
            incremental=args.incremental,
            propagator=propagator,
            solver=solver,
        )
    )
)

for backdoor in backdoors:
    cell.touch().log('\n'.join('-- ' + s for s in str(monte_carlo).split('\n')))
    cell.log('------------------------------------------------------')
    cell.log('Iteration: 0', '------------------------------------------------------')
    cell.log('Run predictor for backdoor: %s' % backdoor, 'With %d cases:' % args.sampling)
    value = monte_carlo.predict(backdoor, count=args.sampling)
    cell.log('End prediction with value: %.7g' % value)
    cell.log('------------------------------------------------------')

cell.close()
