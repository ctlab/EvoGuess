import argparse

from numpy.random.mtrand import RandomState
from pysat import solvers

from output import *
from predictor import *
from predictor.instance.models.var import Backdoor

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('instance', type=str, help='instance of problem')
parser.add_argument('backdoors', type=str, help='load backdoor from specified file')
parser.add_argument('-i', '--incremental', action='store_true', help='incremental mode')
parser.add_argument('-d', '--description', metavar='str', default='', type=str, help='launch description')
parser.add_argument('-c', '--count', metavar='1000', type=int, default=1000, help='count of generated tasks')
parser.add_argument('-v', '--verbosity', metavar='0', type=int, default=0, help='debug [0-3] verbosity level')

args = parser.parse_args()

inst = instance.A5_1()
assert inst.check()

backdoors = Backdoor.load(args.backdoors)

cell = Cell(
    path=['output', '_check_logs', inst.tag],
    logger=tools.logger(),
    debugger=tools.debugger(verb=args.verbosity)
).open(description=args.description)

rs = RandomState()
predictor = Predictor(
    rs=rs,
    output=cell,
    instance=inst,
    method=method.InverseBackdoorSets(
        time_limit=10,
        chunk_size=10000,
        concurrency=concurrency.pysat.PebbleMap(
            threads=32,
            incremental=args.incremental,
            solver=solvers.MapleChrono,
            propagator=solvers.MapleChrono,
        )
    )
)

for backdoor in backdoors:
    cell.touch().log('\n'.join('-- ' + s for s in str(predictor).split('\n')))
    cell.log('------------------------------------------------------')
    cell.log('Iteration: 0', '------------------------------------------------------')
    cell.log('Run predictor for backdoor: %s' % backdoor, 'With %d cases:' % args.count)
    value = predictor.predict(backdoor, args.count)
    cell.log('End prediction with value: %.7g' % value)
    cell.log('------------------------------------------------------')

cell.close()
