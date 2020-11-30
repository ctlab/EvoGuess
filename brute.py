import json
import argparse
from multiprocessing import Pool

from pysat import solvers as slvs

import instance

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
parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')

args = parser.parse_args()

max_tasks = 100
length = args.l
threads = args.t
bds_path = args.bds
stats_keys = [
    'time',
    'conflicts',
    'propagations',
    'learned_literals'
]
_instance = instance.get_instance(args.instance)

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
        if status is None:
            measures.append(None)
        else:
            stats = solver.accum_stats()
            stats['time'] = solver.time()
            measures.append({key: stats[key] for key in stats_keys})
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

        if all([m is not None for m in measures]):
            summary = {}
            for stats_key in stats_keys:
                summary[stats_key] = sum([measure[stats_key] for measure in measures])

            str_info = json.dumps({'summary': summary, 'measures': measures})
            print("[%s]: %s" % (bd_str, str_info))
            results[0].append((bd, measures, summary))
        else:
            print("[%s]: Bad measures (%s)" % (bd_str, json.dumps(measures)))
            results[1].append((bd, measures))


def test():
    n = len(_instance.secret_key)
    res_list, results = [], ([], [])
    pool = Pool(processes=threads)
    print("Solver: %s" % args.solver)
    print("Measures: %s" % stats_keys)
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

        res = pool.apply_async(worker_f, (_instance, backdoor))
        res_list.append((backdoor, res))

    while len(res_list) > 0:
        handle(res_list, results)

    for stats_key in stats_keys:
        print("\nSorted: (%s)" % stats_key)
        for bd, _, summary in sorted(results[0], key=lambda x: x[2][stats_key]):
            print("[%s]: %s" % (','.join(map(str, bd)), summary[stats_key]))

    print("\nErrors: %d" % len(results[1]))


if __name__ == "__main__":
    test()
