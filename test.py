import argparse

from copy import copy
from time import time as now
from pysat import solvers as slvs
from numpy.random.mtrand import RandomState

from method.concurrency.models import Task
from method.instance.models.var import Backdoor
from output import *
from method import *

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
parser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')

parser.add_argument('-tl', metavar='5', type=int, default=5, help='time limit for ibs')
parser.add_argument('-n', '--sampling', metavar='1000', type=int, default=1000, help='estimation sampling')
parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
parser.add_argument('-pr', '--propagator', metavar='str', type=str, default='', help='SAT-solver to propagate')

args = parser.parse_args()

inst = instance.get(args.instance)
assert inst.check(), "Cnf is missing"

solver = solvers[args.solver]
propagator = solvers[args.propagator] if args.propagator else solver

cell = Cell(
    path=['output', '_test_logs', inst.tag],
    largs={},
    dargs={
        'dall': True,
        'verb': 10
    },
).open().touch()

concur = concurrency.pysat.PebbleMap(
    threads=args.threads,
    incremental=False,
    propagator=propagator,
    solver=solver,
    # keep=True
)

concur_incr = concurrency.pysat.PebbleMap(
    threads=args.threads,
    incremental=True,
    propagator=propagator,
    solver=solver,
    # keep=True
)

kwargs = {
    'output': cell,
    'instance': inst
}

rs = RandomState()
count = args.sampling
# backdoor = Backdoor.parse('1 3 4 5 7 9 10 13 16 18 19 20 21 22 23 24 25 26 27 30 31 34 37 41 43 44 47 48 50 51 52 56 60 61 64')
backdoor = Backdoor.parse('2 4 6 9 11 16 20 23 24 25 26 27 28 30 32 36 38 46 47 48 51')
while True:
    init_tasks = [Task(i, proof=True, sk=inst.secret_key.values(rs=rs)) for i in range(count)]
    inited = concur.propagate(init_tasks, **kwargs)

    assert len(inited) == count, "Init result len less then count"

    tasks = []
    for result in inited:
        tasks.append(Task(result.i, tl=args.tl, bd=backdoor.values(solution=result.solution),
                          **inst.values(result.solution)))

    tasks_incr = [copy(t) for t in tasks]

    timestamp = now()
    results = concur.solve(tasks, **kwargs)
    time = now() - timestamp

    assert len(results) == count, "Result len less then count"

    timestamp = now()
    results_incr = concur_incr.solve(tasks_incr, **kwargs)
    time_incr = now() - timestamp

    assert len(results_incr) == count, "Incr result len less then count"

    good, bad = 0, 0
    for i in range(count):
        s = '%s(%.2f)' % (results[i].get_status(), results[i].time)
        s_incr = '%s(%.2f)' % (results_incr[i].get_status(), results_incr[i].time)

        if results[i].status is None and results_incr[i].status is not None:
            good += 1
        if results_incr[i].status is None and results[i].status is not None:
            bad += 1
        print('%d: %s -> %s' % (results[i].i, s, s_incr))

    print('Time:', time)
    print('Time incr:', time_incr)
    print('Bad:', bad)
    print('Good:', good)
    break
