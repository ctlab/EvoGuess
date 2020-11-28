import json
from math import sqrt
from operator import itemgetter
from os.path import join
from time import time as now

from output.parser.impl.base import BaseParser
from structure.data.individual_top import IndividualsTop

base_path = './output/_main_logs/sgen/6_900_100/'
test_runs = [
    # '2020.11.22_15:05:07-2020.11.22_16:09:43',
    # '2020.11.23_16:17:53-2020.11.23_17:23:22',  # multi
    # '2020.11.28_10:21:21-2020.11.28_11:25:39',  # multi
    # '2020.11.28_11:18:04-2020.11.28_12:22:15'  # no multi
    '2020.11.28_13:22:04-2020.11.28_14:30:01'  # no multi genetic
    # '2020.11.28_13:27:02-2020.11.28_14:37:01'  # multi genetic
]

# base_path = './output/_main_logs/pancake_vs_selection/4x7/'
# test_runs = [
#     # '2020.11.23_19:12:52-2020.11.23_20:13:54',  # multi
#     '2020.11.27_14:24:12-2020.11.27_15:25:56',  # multi
#     '2020.11.27_15:26:47-2020.11.27_16:28:33'  # no multi
# ]

full_timestamp = now()
pr = BaseParser()
for run in test_runs:
    path = join(base_path, run)
    its, time_range = pr.parse(path)

    cache = {}
    top = IndividualsTop()

    best = None
    cores = {}
    for i, it in enumerate(its):
        print('Processing %d iterations (of %d)' % (i + 1, len(its)))
        for ind in it:
            key = str(ind.backdoor)
            if key not in cache:
                cache[key] = ind.value
                top.check(ind)
                for case in ind.get('cases'):
                    pid = case[1]
                    if pid not in cores:
                        cores[pid] = []
                    cores[pid].append(case[4])

    for ind in top.list():
        print(len(ind.backdoor))

    for ind in top.list():
        print(' '.join(map(str, ind.backdoor.list)))

    for ind in top.list():
        if 2 ** len(ind.backdoor) == ind.get('count'):
            print('%s\t-' % str(ind.value).replace('.', ','))
        else:
            print('-\t %s' % str(ind.value).replace('.', ','))

    core_full_time = {}
    for pid, times in cores.items():
        core_full_time[pid] = 0
        # print(pid, len(times))
        for t1, t2 in times:
            core_full_time[pid] += t2 - t1

    alg_time = time_range[1] - time_range[0]
    sft = sorted(core_full_time.items(), key=itemgetter(1))

    mid = len(core_full_time) // 2
    print('Min time: %.2f (%.2f%%) for %d' % (sft[0][1], 100 * sft[0][1] / alg_time, sft[0][0]))
    print('Max time: %.2f (%.2f%%) for %d' % (sft[-1][1], 100 * sft[-1][1] / alg_time, sft[-1][0]))
    print('Mid time: %.2f (%.2f%%) for %d' % (sft[mid][1], 100 * sft[mid][1] / alg_time, sft[mid][0]))

    full_time = sum(time for _, time in sft)
    avg_time = full_time / len(core_full_time)
    dis_time = sum((time - avg_time) ** 2 for _, time in sft) / len(core_full_time)
    print('Avg time: %.2f +- %.2f (%.2f%% +- %.2f%%)' % (
        avg_time, sqrt(dis_time),
        100 * avg_time / alg_time,
        100 * sqrt(dis_time) / alg_time
    ))

    with open('no_test.json', 'w+') as f:
        f.write(json.dumps(cores, indent=2))

print(now() - full_timestamp)
