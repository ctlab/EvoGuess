import argparse

from numpy.random.mtrand import RandomState
from pysat import solvers

from output import *
from algorithm import *
from predictor import *

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')
parser.add_argument('-wt', '--walltime', metavar='hh:mm:ss', type=str, default='24:00:00', help='wall time')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')

args = parser.parse_args()

inst = instance.A5_1()
assert inst.check()

cell = Cell(
    path=['output', '_logs', inst.tag],
    logger=tools.logger(),
    debugger=tools.debugger(verb=args.verbosity)
).open(description=args.description).touch()

rs = RandomState()
predictor = Predictor(
    rs=rs,
    output=cell,
    instance=inst,
    method=method.InverseBackdoorSets(
        time_limit=10,
        chunk_size=1000,
        concurrency=concurrency.PySATPool(
            threads=32,
            incremental=False,
            solver=solvers.MapleChrono,
            propagator=solvers.MapleChrono,
        )
    )
)

algorithm = Evolution(
    output=cell,
    predictor=predictor,
    stagnation_limit=100,
    sampling=sampling.Const(500),
    limit=limit.WallTime(args.walltime),
    strategy=strategy.Plus(
        mu=1, lmbda=1,
        selection=selection.Roulette(),
        mutation=mutation.Uniform(),
        crossover=crossover.Uniform(p=0.2)
    )
)

points = algorithm.start(inst.secret_key.to_backdoor())
cell.close()
