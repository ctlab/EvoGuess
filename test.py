import re
import tarfile
from os.path import join

from output.parser.impl.base import BaseParser
from structure.data.individual_top import IndividualsTop

base_path = './output/_main_logs/sgen/6_900_100/'
g3_plus_runs = [
    '2020.10.10_20:34:59-2020.10.11_08:35:01',
    '2020.10.12_15:37:58-2020.10.13_03:38:44',
    '2020.10.23_06:18:18-2020.10.23_18:23:18',
    '2020.10.23_09:45:11-2020.10.23_21:48:28'
]
g3_elitism_runs = [
    '2020.10.24_11:04:11-2020.10.24_23:08:02',
    '2020.10.25_00:56:11-2020.10.25_12:59:33',
    '2020.10.25_12:07:14-2020.10.26_00:12:00',
    '2020.10.26_01:11:17-2020.10.26_13:15:24'
]

cd_plus_runs = [
]
cd_elitism_runs = [
    '2020.11.01_16:26:19-2020.11.02_04:32:46',
    '2020.11.01_16:24:16-2020.11.02_04:51:40'
]

base_path = './output/_main_logs/sgen/6_1200_5-1/'
g3_plus_1200_runs = [
    '2020.10.27_09:50:16-2020.10.27_21:55:29',
    '2020.10.31_10:39:26-?',
]
g3_elitism_1200_runs = [
    '2020.10.29_09:15:26-?',
    '2020.10.30_14:24:35-?'
]
cd_plus_1200_runs = [
    '2020.10.28_14:27:19-2020.10.29_02:42:30',
    '2020.10.31_10:36:07-2020.10.31_23:07:03',
]
cd_elitism_1200_runs = [
    '2020.10.30_14:35:41-2020.10.31_03:04:48',
    '2020.10.28_14:31:14-2020.10.29_03:29:04'
]

test_runs = [
    '2020.11.01_15:59:30-2020.11.01_17:01:08',
    # '2020.11.01_16:03:19-2020.11.01_17:05:33',
    # '2020.11.02_14:46:18-2020.11.02_16:20:12',
    # '2020.11.02_14:44:22-2020.11.02_15:46:01',
    '2020.11.02_16:41:18-2020.11.02_17:47:51',
    # '2020.11.02_16:43:26-2020.11.02_17:44:34',
    '2020.11.02_18:44:10-2020.11.02_19:46:03',
    # '2020.11.02_18:40:17-2020.11.02_19:42:45',
]

base_path = './output/_check_logs/sgen/6_1200_5-1/'
test2_run = [
    # '2020.11.03_20:06:35-2020.11.03_22:55:03',
    '2020.11.03_21:20:27-2020.11.03_23:33:06',
    # '2020.11.04_01:16:23-2020.11.04_17:00:41'
]


def get_values():
    bd_file = join(path, 'backdoors.tar.gz')
    backdoors = tarfile.open(bd_file, 'r:gz')

    all_values = []
    for member in backdoors.getmembers():
        f = backdoors.extractfile(member)
        if f is not None:
            content = f.read().decode('utf-8')
            case_count = re.findall(r'Cases \((\d*)\):', content)
            values = re.findall(r'\'propagations\': (\d*)', content)
            backdoor_key = re.findall(r'Backdoor: (\[[ \d]*]\(\d*\))', content)
            assert int(case_count[0]) == len(values)
            all_values.append((backdoor_key[0], [int(value) for value in values]))

    return all_values


def get_times():
    bd_file = join(path, 'backdoors.tar.gz')
    backdoors = tarfile.open(bd_file, 'r:gz')

    job_times, process_times = [], []
    for member in backdoors.getmembers():
        f = backdoors.extractfile(member)
        if f is not None:
            content = f.read().decode('utf-8')
            job_time = re.findall(r'Job time: (\d*)', content)
            if len(job_time) > 0:
                job_times.append(float(job_time[0]))

            process_time = re.findall(r'Process time: (\d*)', content)
            if len(process_time) > 0:
                process_times.append(float(process_time[0]))

    return job_times, process_times


pr = BaseParser()
for run in test2_run:
    path = join(base_path, run)
    its = pr.parse(path)
    cache = {}
    top = IndividualsTop()

    best = None
    for it in its:
        for ind in it:
            key = str(ind.backdoor)
            cache[key] = ind.value
            top.check(ind)

    # job_times, process_times = get_times()
    # print('Sum job time: %f' % (sum(job_times) / 3600))
    # print('Sum process time: %f' % (sum(process_times) / 3600))
    for backdoor, values in get_values():
        distribution = {}
        # for value in values:
        #     if value in distribution:
        #         distribution[value] += 1
        #     else:
        #         distribution[value] = 1
        print(backdoor, sum(values), distribution)

    print('Uniq points: %d' % len(cache))
    for ind in top.list():
        print(len(ind.backdoor))

    for ind in top.list():
        print(' '.join(map(str, ind.backdoor.list)))

    for ind in top.list():
        print(str(ind.value).replace('.', ','))

    print('\n')
