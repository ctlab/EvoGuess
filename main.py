import argparse

from numpy.random.mtrand import RandomState
# from pysat import solvers

from output import *
from algorithm import *
from predictor import *

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('cipher', type=str, help='cryptographic cipher')

parser.add_argument('-wt', '--walltime', metavar='hh:mm:ss', type=str, default='24:00:00', help='wall time')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')

args = parser.parse_args()

cell = Cell(
    path=['output', '_logs', 'test', args.cipher],
    logger=tools.logger(),
    debugger=tools.debugger(verb=args.verbosity)
).open(description=args.description)

rs = RandomState()
a5_1 = cipher.A5_1()
predictor = Predictor(
    rs=rs,
    output=cell,
    cipher=a5_1,
    method=method.GuessAndDetermine(
        # time_limit=5,
        chunk_size=1000,
        concurrency=concurrency.SinglePool(
            threads=4,
            solver=solver.Lingeling(interrupter=solver.interrupter.Timelimit(tl=10)),
            propagator=solver.Lingeling(interrupter=solver.interrupter.Base(tl=0)),
        )
    )
)

algorithm = Evolution(
    output=cell,
    predictor=predictor,
    sampling=sampling.Const(500),
    limit=limit.WallTime(args.walltime),
    strategy=strategy.Plus(
        mu=1, lmbda=1,
        selection=selection.Roulette(),
        mutation=mutation.Uniform(),
        crossover=crossover.Uniform(p=0.2)
    )
)

points = algorithm.start(a5_1.secret_key.to_backdoor())

cell.close()
