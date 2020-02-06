import argparse

from numpy.random.mtrand import RandomState
from pysat import solvers

from output import *
from algorithm import *
from predictor import *

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('instance', type=str, help='instance of problem')
parser.add_argument('-i', '--incremental', action='store_true', help='incremental mode')
parser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')
parser.add_argument('-wt', '--walltime', metavar='hh:mm:ss', type=str, default='24:00:00', help='wall time')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')

args = parser.parse_args()

inst = instance.get(args.instance)
assert inst.check()

cell = Cell(
    path=['output', '_logs', inst.tag],
    logger=tools.logger(),
    debugger=tools.debugger(verb=args.verbosity)
).open(description=args.description).touch()

rs = RandomState()
predictor = MonteCarlo(
    rs=rs,
    output=cell,
    instance=inst,
    method=method.InverseBackdoorSets(
        time_limit=5,
        chunk_size=1000,
        corrector=method.corrector.Ruler(limiter=0.01),
        concurrency=concurrency.pysat.PebbleMap(
            threads=args.threads,
            incremental=args.incremental,
            solver=solvers.Glucose4,
            propagator=solvers.Glucose4,
        )
    )
)

algorithm = Evolution(
    output=cell,
    predictor=predictor,
    stagnation_limit=155,
    sampling=sampling.Const(500),
    limit=limit.tools.Any(
        limit.Stagnation(150),
        limit.WallTime(args.walltime),
    ),
    strategy=strategy.Plus(
        mu=1, lmbda=1,
        selection=selection.Best(),
        mutation=mutation.Uniform(),
        crossover=crossover.Uniform(p=0.2)
    )
)

points = algorithm.start(inst.secret_key.to_backdoor())
cell.close()
