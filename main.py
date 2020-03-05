import argparse
import re

from numpy.random.mtrand import RandomState
from pysat import solvers as slvs

from output import *
from algorithm import *
from predictor import *

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
parser.add_argument('method', type=str, help='method of estimation')
parser.add_argument('-i', '--incremental', action='store_true', help='incremental mode')
parser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')
parser.add_argument('-d', '--description', metavar='str', type=str, default='', help='launch description')
parser.add_argument('-wt', '--walltime', metavar='hh:mm:ss', type=str, default='24:00:00', help='wall time')
parser.add_argument('-v', '--verbosity', metavar='3', type=int, default=3, help='debug [0-3] verbosity level')

parser.add_argument('-tl', metavar='5', type=int, default=5, help='time limit for ibs')
parser.add_argument('-n', '--sampling', metavar='1000', type=int, default=1000, help='estimation sampling')
parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
parser.add_argument('-pr', '--propagator', metavar='str', type=str, default='', help='SAT-solver to propagate')

parser.add_argument('-a', '--algorithm', metavar='str', type=str, default='1+1', help='optimization algorithm')
parser.add_argument('-st', '--stagnation', metavar='300', type=int, default=300, help='stagnation limit')

args = parser.parse_args()

inst = instance.get(args.instance)
assert inst.check(), "Cnf is missing"

Method = method.get(args.method)
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
    path=['output', '_logs', inst.tag],
    largs={},
    dargs={
        'dall': True,
        'verb': args.verbosity
    },
).open(description=args.description).touch()

rs = RandomState()
predictor = MonteCarlo(
    rs=rs,
    output=cell,
    instance=inst,
    method=Method(
        time_limit=args.tl,
        chunk_size=1000,
        save_init=True,
        reset_init=10,
        corrector=method.corrector.Ruler(limiter=0.01),
    ),
    concurrency=concurrency.pysat.PebbleMap(
        threads=args.threads,
        incremental=args.incremental,
        propagator=propagator,
        solver=solver,
    )
)

algorithm = Evolution(
    output=cell,
    predictor=predictor,
    stagnation_limit=args.stagnation,
    sampling=sampling.Const(args.sampling),
    limit=limit.WallTime(args.walltime),
    strategy=Strategy(
        mu=mu, lmbda=lmbda,
        selection=selection.Best(),
        mutation=mutation.Uniform(),
        crossover=crossover.Uniform(p=0.2)
    )
)

points = algorithm.start(inst.secret_key.to_backdoor())
cell.close()
