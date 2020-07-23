import argparse
from threading import Timer
from time import sleep

import numpy as np
from time import time as now
from pysat import solvers as slvs
from multiprocessing import Pool, TimeoutError

from method import *
from method.instance.models.var import Backdoor

parser = argparse.ArgumentParser(description='EvoGuess')
parser.add_argument('-t', metavar='36', type=int, default=36, help='threads')
parser.add_argument('-tl', metavar='1.0', type=float, default=1., help='tl')
parser.add_argument('-r', metavar='100', type=int, default=100, help='repeats')

args = parser.parse_args()

tl = args.tl
repeats = args.r
threads = args.t

print(threads, tl, repeats)
Solver = slvs.Glucose4
s_kg = 'asg72'
s_bd = '1 3 6 8 11 13 15 16 17 46'


def worker_f(inst, init_sol, backdoor, count, tl):
    assumptions = []
    for values in inst.values(solution=init_sol).values():
        assumptions.extend(values)

    ans, statuses = None, []
    variables = backdoor.snapshot()
    for value in range(count[0], count[1]):
        solver = Solver(bootstrap_with=inst.clauses())

        values = [1 if value & (1 << i) else 0 for i in range(len(backdoor))][::-1]
        bd = [x if values[j] else -x for j, x in enumerate(variables)]

        timer = Timer(tl, solver.interrupt, ())
        timer.start()

        timestamp = now()
        status = solver.solve_limited(assumptions=assumptions + bd)
        time = now() - timestamp

        if timer.is_alive():
            timer.cancel()
        else:
            solver.clear_interrupt()

        solution = solver.get_model() if status else None
        statuses.append((value, status))
        solver.delete()

        if status:
            ans = (solution, time)
            break

    return statuses, ans


rs = np.random.RandomState()

inst = instance.get(s_kg)
assert inst.check()

backdoor = Backdoor(list(map(int, s_bd.split(' '))))
print(backdoor)

successes, fails = [], []
for k in range(repeats):
    # init
    sk = inst.secret_key.values(rs=rs)
    solver = Solver(bootstrap_with=inst.clauses())
    status = solver.solve(assumptions=sk)
    init_sol = solver.get_model() if status else None

    # main
    pool = Pool(processes=threads)

    count = 2 ** len(backdoor)
    t_count, remainder = divmod(count, threads)
    counts, j = [], 0
    for i in range(threads):
        bound = t_count + (1 if remainder > i else 0)
        counts.append((j, j + bound))
        j += bound

    res_list = []
    timestamp = now()
    for count in counts:
        res = pool.apply_async(worker_f, (inst, init_sol, backdoor, count, tl))
        res_list.append(res)

    answer, results = None, []
    active = [True] * threads
    while len(results) < threads:
        if answer is not None: break

        for i, res in enumerate(res_list):
            if not active[i]: continue
            try:
                result = res.get(timeout=0.2)
                statuses, ans = result
                results.append(statuses)
                active[i] = False

                if ans is not None:
                    answer = ans
            except TimeoutError:
                pass

    time = (now() - timestamp) * threads
    pool.terminate()
    sleep(tl)
    pool.join()

    if answer is not None:
        real_sk = ''.join(['0' if var < 0 else '1' for var in sk])

        found_vars = inst.secret_key.values(solution=answer[0])
        found_sk = ''.join(['0' if var < 0 else '1' for var in found_vars])
        successes.append((real_sk, found_sk, time, answer[1]))
    else:
        fails.append((sum([len(result) for result in results]), time))

    print('%d / %d (%.1f s)' % (k + 1, repeats, time))

if len(successes) > 0:
    print('Successes:')
    for r_sk, f_sk, time, c_time in successes:
        print(r_sk == f_sk, time, c_time)

if len(fails) > 0:
    print('\nFails:')
    for fail in fails:
        print(fail)

stat = sum([1 if r == f else 0 for r, f, _, _ in successes])
print('\nSuccess attacks: %d (%.2f %%)' % (stat, 100. * stat / repeats))

wrongs = len(successes) - stat
if wrongs > 0:
    print('Wrong answers: %d (%.2f %%)' % (wrongs, 100. * wrongs / repeats))
    print('\nCollisions:')
    for r_sk, f_sk, time, c_time in successes:
        if r_sk != f_sk:
            print(r_sk, f_sk)

if stat > 0:
    full_time = 0.
    min_time, max_time = tl, 0
    for r_sk, f_sk, time, c_time in successes:
        if r_sk == f_sk:
            full_time += time
            min_time = min(min_time, c_time)
            max_time = max(max_time, c_time)

    ex = full_time / stat
    dx = sum([(time - ex) ** 2 for _, _, time, _ in successes]) / stat
    print('\nAvg success time: %.2f +- %.2f' % (ex, pow(dx, 0.5)))
    print('Case time range: (%.2f, %.2f)' % (min_time, max_time))

if len(fails) > 0:
    ex = sum([time for _, time in fails]) / len(fails)
    dx = sum([(time - ex) ** 2 for _, time in fails]) / len(fails)
    print('\nAvg fail time: %.2f +- %.2f' % (ex, pow(dx, 0.5)))
