import argparse
from multiprocessing import Pool
from operator import itemgetter

from pysat import solvers as slvs

from method import *

solvers = {
    'cd': slvs.Cadical,
    'g3': slvs.Glucose3,
    'g4': slvs.Glucose4,
}

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('instance', type=str, help='instance of problem')
parser.add_argument('-t', metavar='36', type=int, default=36, help='threads')
parser.add_argument('-l', metavar='1', type=int, default=1, help='backdoor length')
parser.add_argument('-bds', metavar='path', type=str, default="", help='backdoors')
parser.add_argument('-g', metavar='0', type=int, default=0, help='group size')
parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')

args = parser.parse_args()

max_tasks = 100
length = args.l
groups = args.g
threads = args.t
bds_path = args.bds
inst = instance.get(args.instance)

Solver = solvers[args.solver]
start = [i + 1 for i in range(length)]


def backdoors(st, mx, limit=None, depth=0):
    counter = 0
    for i in range(st[depth], mx + 1):
        if depth + 1 == len(st):
            yield st[:0] + [i]
        else:
            new_st = st
            if i != st[depth]:
                new_st = st[:depth] + [j for j in range(i, i + len(st) - depth)]
            for bd in backdoors(new_st, mx, limit, depth + 1):
                if counter == limit: break
                if depth == 0: counter += 1
                yield [i] + bd


def worker_f(inst, backdoor):
    measures = []
    for value in range(2 ** len(backdoor)):
        solver = Solver(bootstrap_with=inst.clauses(), use_timer=True)
        values = [1 if value & (1 << i) else 0 for i in range(len(backdoor))][::-1]
        assumptions = [x if values[k] else -x for k, x in enumerate(backdoor)]

        status = solver.solve(assumptions=assumptions)
        # measure = solver.time()
        stats = solver.accum_stats()
        measure = stats.get('conflicts', None)
        measures.append(None if status is None else measure)
        solver.delete()

    return measures


def handle(res_list, results):
    res_list[0][1].wait()
    while len(res_list) > 0 and res_list[0][1].ready():
        bd, res = res_list.pop(0)
        bd_str = ','.join(map(str, bd))
        try:
            measures = res.get()
        except Exception as e:
            print("[%s]: Error (%s)" % (bd, e))
            results[1].append(bd_str, None)
            continue

        str_measures = ["None" if m is None else str(m) for m in measures]
        if all([m is not None for m in measures]):
            summary = sum(measures)
            print("[%s]: %.2f (%s)" % (bd_str, summary, ','.join(str_measures)))
            results[0].append((bd, measures, summary))
        else:
            print("[%s]: Bad measures (%s)" % (bd_str, ','.join(str_measures)))
            results[1].append((bd, measures))


def test():
    n = len(inst.secret_key)
    res_list, results = [], ([], [])
    pool = Pool(processes=threads)
    if len(bds_path) > 0:
        print("Path: %s" % bds_path)
        lines = [line.strip('\n') for line in open(bds_path).readlines()]
        bds = [line.split(' ') if len(line) > 0 else [] for line in lines]
        backdoor_list = [[int(var) for var in bd] for bd in bds]
    else:
        backdoor_list = backdoors(start, n)

    print("Backdoors:")
    for backdoor in backdoor_list:
        while len(res_list) >= max_tasks:
            handle(res_list, results)

        res = pool.apply_async(worker_f, (inst, backdoor))
        res_list.append((backdoor, res))

    while len(res_list) > 0:
        handle(res_list, results)

    if groups > 0:
        print("\nGroups:")
        for i in range(0, len(results[0]), groups):
            group = results[0][i:i + groups]
            for bd, _, summary in sorted(group, key=itemgetter(2)):
                print("[%s]: %.2f" % (','.join(map(str, bd)), summary))
            print('')
    else:
        print("\nSorted:")
        for bd, _, summary in sorted(results[0], key=itemgetter(2)):
            print("[%s]: %.2f" % (','.join(map(str, bd)), summary))

    print("\nErrors: %d" % len(results[1]))


if __name__ == "__main__":
    test()
