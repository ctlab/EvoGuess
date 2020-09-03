from math import sqrt
from pysat import solvers as slvs
from argparse import ArgumentParser
from numpy.random.mtrand import RandomState

from method import *
from output import *
from output import parser

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

argparser = ArgumentParser(description='EvoGuess')
argparser.add_argument('instance', type=str, help='instance of problem')
argparser.add_argument('run', type=str, help='path to log directory')
argparser.add_argument('-t', '--threads', metavar='1', type=int, default=1, help='concurrency threads')
argparser.add_argument('-c', '--count', type=int, default=1, help='count of log\'s files')
argparser.add_argument('-e', '--eps', type=float, default=0.1, help='eps values')
argparser.add_argument('-k', '--tries', type=int, default=1, help='increase tries')

argparser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
argparser.add_argument('-pr', '--propagator', metavar='str', type=str, default='', help='SAT-solver to propagate')

args, _ = argparser.parse_known_args()

inst = instance.get(args.instance)
assert inst.check()

solver = solvers[args.solver]
propagator = solvers[args.propagator] if args.propagator else solver


def _ed(values):
    n = len(values)
    e = sum(values) / n
    d = sum([(value - e) ** 2 for value in values]) / (n - 1)
    return n, e, d


def __eps(values, delta=0.05):
    n, e, d = _ed(values)
    return sqrt(d / (delta * n)) / e


cell = Cell(
    path=['output', '_post_logs', inst.tag],
    largs={},
    dargs={'dall': False, 'verb': 3},
).open(description="").touch()

rs = RandomState()
function = function.GuessAndDetermine(
    chunk_size=16384,
)
concurrency = concurrency.pysat.MapPool(
    solver=solver,
    propagator=propagator,
    incremental=False,
    threads=args.threads,
    measure=concurrency.measure.Propagations(),
)

f_kwargs = {
    'rs': rs,
    'output': cell,
    'instance': inst,
    'concurrency': concurrency
}


def __value(_case, _store):
    key = str(_case.backdoor)
    if key not in _store:
        return _case.value

    _, n_value = _store[key]
    return n_value


def __extend(_bd, _res, _store):
    real_count = 2 ** len(_bd)
    key, count = str(_bd), len(_res)
    if 2.1 * count >= real_count:
        results = function.verify(_bd, real_count, 0, **f_kwargs)
    else:
        results = function.evaluate(_bd, [], count, **f_kwargs) + _res

    info = function.calculate(_bd, results, output=cell)
    _store[key] = results, info.value

    return results, info.value


def __check(_case, _store):
    real_count = 2 ** len(_case.backdoor)
    c_res, c_val = _case.results, _case.value

    for tr in range(args.tries):
        if len(c_res) == real_count: break
        if __eps([res.value for res in c_res]) <= args.eps: break
        c_res, c_val = __extend(_case.backdoor, c_res, store)

    return c_res, c_val


iterations = []
pr = parser.LogParser()
for j in range(args.count):
    path = 'output/_new_logs/%s/%s/log_%d' % (inst.tag, args.run, j)
    _, its = pr.parse_file(path)
    iterations.extend(its)

store = {}
best = iterations[0][0]
cell.log('\n'.join('-- ' + s for s in '\n'.join(map(str, [
    'Algorithm: Post',
    'Run: %s' % args.run,
    'Eps: %f' % args.eps,
    'Count: %d' % args.count,
    'Tries: %d' % args.tries,
    concurrency,
    inst,
    function,
])).split('\n')), '------------------------------------------------------')
cell.log('Iteration: 0', '------------------------------------------------------')

b_results, b_value = __check(best, store)
cell.log('Run method on backdoor: %s' % best.backdoor, 'With %d cases:' % len(b_results))
cell.log(*list(map(str, b_results)))
cell.log('{}')
cell.log('Spent time: %.2f s' % best.cpu_time, 'End with value: %.7g' % b_value)
cell.log('------------------------------------------------------')

for i in range(1, len(iterations)):
    cell.log('Iteration: %d' % i)
    print(i, '/', len(iterations))
    for j, case in enumerate(iterations[i]):
        cell.log('------------------------------------------------------')
        if case.cpu_time < 0:
            cell.log('Hashed backdoor: %s' % case.backdoor, 'With value: %.7g\n' % __value(case, store))
            continue

        if b_value > case.value:
            c_results, c_value = __check(case, store)
            if b_value > c_value:
                best = case
                b_value = c_value
                b_results = c_results

            cell.log('Run method on backdoor: %s' % case.backdoor, 'With %d cases:' % len(c_results))
            cell.log(*list(map(str, c_results)))
            cell.log('{}')
            cell.log('Spent time: %.2f s' % case.cpu_time, 'End with value: %.7g' % c_value)
        else:
            cell.log('Run method on backdoor: %s' % case.backdoor, 'With %d cases:' % len(case.results))
            cell.log(*list(map(str, case.results)))
            cell.log('{}')
            cell.log('Spent time: %.2f s' % case.cpu_time, 'End with value: %.7g' % case.value)

    cell.log('------------------------------------------------------')

cell.log('------------------------------------------------------', 'Points:', '%s by %.7g' % (best.backdoor, b_value))
cell.close()
