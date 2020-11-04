from time import sleep

from method import solver
from multiprocessing import Pool

import instance

THREADS = 36

solvers = ['cd', 'g3', 'g4']
instances = [
    'sgen:6_200_5-1',
    'sgen:6_150_100',
    'sgen:6_150_200',
    'sgen:6_150_300',
    'sgen:6_150_1001',
]
instances.extend(['bvi:%d_8' % i for i in range(3, 9)])
instances.extend(['bvi:8_16', 'bvi:8_64'])

for j in range(4, 11):
    instances.extend(['bvp:%d_%d' % (i, j) for i in range(3, 9)])

for j in range(5, 9):
    instances.extend(['bvs:%d_%d' % (i, j) for i in range(3, 9)])
for j in range(12, 16):
    instances.extend(['bvs:%d_%d' % (i, j) for i in range(3, 6)])
instances.extend(['bvs:8_4', 'bvs:4_9'])

for j in range(4, 11):
    instances.extend(['pvs:%d_%d' % (i, j) for i in range(3, 9)])


def worker_f(k, inst, solver_key):
    _solver = solver.pysat.get(solver_key)

    status, stats, _, _ = _solver.solve(inst.clauses(), [])
    return k, status, stats


def check():
    res_list, results = [], {}
    pool = Pool(processes=THREADS)

    k = 0
    for instance_key in instances:
        for solver_key in solvers:
            _instance = instance.get_instance(instance_key)

            res = pool.apply_async(worker_f, (k, _instance, solver_key))
            res_list.append((k, instance_key, solver_key, res))
            k += 1

    j, tick, debug_ticks = 0, 1.0, 10
    while len(res_list) > 0:
        i = 0
        while i < len(res_list):
            if res_list[i][3].ready():
                k, inst_key, slv_key, res = res_list.pop(i)

                try:
                    task_result = res.get()
                except Exception as e:
                    print("[ERROR] Error on %s with %s (%s)" % (inst_key, slv_key, e))
                    continue

                print("[LOG] (%s, %s): %s" % (slv_key, inst_key, task_result))
                if inst_key in results:
                    results[inst_key][slv_key] = task_result
                else:
                    results[inst_key] = {
                        slv_key: task_result
                    }

            sleep(tick)
            j = (j + 1) % debug_ticks
            if j == 0:
                print("[INFO] Left %d task(s)" % len(res_list))

    for inst_key, inst_res in results.items():
        print("\nResults for %s:" % instance.get_instance(inst_key))
        for slv_key, task_res in inst_res.items():
            print("-- %s: %s" % (slv_key, task_res[2]))
        print()


if __name__ == '__main__':
    check()
