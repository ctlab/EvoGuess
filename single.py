from time import sleep

from method import solver
from multiprocessing import Pool

import instance

THREADS = 36

solvers = ['cd', 'g3', 'g4']
instances = [
    'sgen:6_200_1',
    'sgen:6_200_201',
    'pvs:5_7',
    'pvs:6_7',
    'pvs:7_7',
    'pvs:8_7',
    'pvs:4_8',
]


def worker_f(k, inst, solver_key):
    _solver = solver.pysat.get(solver_key)

    status, stats, _, _ = _solver.solve(inst.clauses(), [])
    return k, status, stats


def check():
    res_list, results = [], {}
    pool = Pool(processes=THREADS)

    k = 0
    for instance_key in instances:
        _instance = instance.get_instance(instance_key)
        for solver_key in solvers:
            res = pool.apply_async(worker_f, (k, _instance, solver_key))
            res_list.append((k, instance_key, solver_key, res))
            k += 1

    j, tick, debug_ticks = 0, 1.0, 1000
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

            i += 1

        sleep(tick)
        j = (j + 1) % debug_ticks
        if j == 0:
            with open('single.info', 'a+') as f:
                f.write("[INFO] Left %d task(s)\n" % len(res_list))

    for inst_key, inst_res in results.items():
        print("\nResults for %s:" % instance.get_instance(inst_key))
        for slv_key, task_res in inst_res.items():
            print("-- %s: %s" % (slv_key, task_res[2]))
        print()


if __name__ == '__main__':
    check()
