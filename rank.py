import re
import argparse

from numpy.random.mtrand import RandomState
from pysat import solvers as slvs

from output import *
from method import *
from algorithm import *

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
parser.add_argument('-i', '--incremental', action='store_true', help='incremental mode')
parser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')
parser.add_argument('-d', '--description', metavar='str', type=str, default='', help='launch description')
parser.add_argument('-wt', '--walltime', metavar='hh:mm:ss', type=str, default='24:00:00', help='wall time')
parser.add_argument('-v', '--verbosity', metavar='3', type=int, default=3, help='debug [0-3] verbosity level')
parser.add_argument('-dall', '--debug_all', action='store_true', help='debug on all nodes')

parser.add_argument('-tl', metavar='5', type=int, default=5, help='time limit for ibs')
parser.add_argument('-n', '--sampling', metavar='1000', type=int, default=1000, help='estimation sampling')
parser.add_argument('-sn', '--step_size', metavar='100', type=int, default=100, help='stat test step size')
parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
parser.add_argument('-pr', '--propagator', metavar='str', type=str, default='', help='SAT-solver to propagate')

parser.add_argument('-a', '--algorithm', metavar='str', type=str, default='1+1', help='optimization algorithm')
parser.add_argument('-st', '--stagnation', metavar='300', type=int, default=300, help='stagnation limit')

args = parser.parse_args()

inst = instance.get(args.instance)
assert inst.check(), "Cnf is missing"

Function = function.get(args.function)
solver = solvers[args.solver]
propagator = solvers[args.propagator] if args.propagator else solver

Strategy = None
exps = [r'(\d+)(\+)(\d+)', r'(\d+)(,)(\d+)', r'(\d+)(\^)(\d+)']
alg_re = [re.findall(exp, args.algorithm) for exp in exps]
for i, alg_args in enumerate(alg_re):
    if len(alg_args):
        mu, op, lmbda = alg_args[0]
        Strategy = strategy.get(op)
        mu, lmbda = map(int, (mu, lmbda))

assert Strategy, "Unknown strategy"

cell = Cell(
    path=['output', '_test_logs', inst.tag],
    largs={},
    dargs={
        'dall': args.debug_all,
        'verb': args.verbosity
    },
).open(description=args.description).touch()

rs = RandomState()
method = RankMonteCarlo(
    rs=rs,
    output=cell,
    instance=inst,
    can_cache=False,
    function=Function(
        time_limit=args.tl,
        chunk_size=1000,
        corrector=function.corrector.Ruler(limiter=0.01),
    ),
    concurrency=concurrency.pysat.PebbleMap(
        threads=args.threads,
        incremental=args.incremental,
        propagator=propagator,
        solver=solver,
    )
)

algorithm = RankEvolution(
    output=cell,
    method=method,
    limit=limit.tools.Any(
        limit.WallTime(args.walltime),
        limit.Stagnation(350),
    ),
    sampling=sampling.Const(args.sampling),
    stat_test=stat_test.MannWhitneyu(
        bound=0.05,
        step_size=args.step_size
    ),
    stagnation_limit=args.stagnation,
    strategy=Strategy(
        mu=mu, lmbda=lmbda,
        selection=selection.Best(),
        mutation=mutation.Doer(beta=3),
        crossover=crossover.Uniform(p=0.2)
    )
)

points = algorithm.start(inst.secret_key.to_backdoor())

cell.close()