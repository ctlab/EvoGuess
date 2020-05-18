import argparse
import subprocess

from multiprocessing import Pool
from pysat.solvers import Cadical, Glucose3

from method import *

parser = argparse.ArgumentParser(description='Test')
parser.add_argument('-t', '--threads', metavar='4', type=int, default=4, help='concurrency threads')
parser.add_argument('-b', metavar='14', type=int, default=14, help='task type')

args = parser.parse_args()

# tag = 'b21'
# p = subprocess.Popen(['ls', '-l', 'templates/Circuit/itc99/%s' % tag], encoding='utf8', stdout=subprocess.PIPE)
# output, _ = p.communicate()
# count = 0
# for line in output.split('\n'):
#     if tag in line:
#         s = line.split('_Cmut')[1].split('.cnf')[0]
#         args = s[:-1], s[-1:]
#         print('(\'%sC:%s_%s\', \'g3\'),' % (tag, args[0], args[1]))
#         count += 1
# print(count)
# exit(0)


def worker_function(f_args):
    inst = instance.get(f_args[0])
    if not inst.check():
        return f_args, None, None, 'Cnf is missing'

    solver = None
    if f_args[1] == 'cd':
        solver = Cadical(bootstrap_with=inst.clauses(), use_timer=True)
    else:
        solver = Glucose3(bootstrap_with=inst.clauses(), use_timer=True)

    if solver is None:
        return f_args, None, None, 'Unknown solver'

    status = solver.solve()
    time = solver.time()
    key = str(solver)
    solver.delete()
    return f_args, time, status, key


pool = Pool(processes=args.threads)

# 30
tasks14 = [
    ('b14C:4060_n', 'cd'),
    ('b14C:4062_p', 'cd'),
    ('b14C:4064_n', 'cd'),
    ('b14C:4102_p', 'cd'),
    ('b14C:4104_n', 'cd'),
    ('b14C:4106_n', 'cd'),
    ('b14C:4108_n', 'cd'),
    ('b14C:4108_p', 'cd'),
    ('b14C:4110_n', 'cd'),
    ('b14C:4112_p', 'cd'),
    ('b14C:4128_p', 'cd'),
    ('b14C:4138_p', 'cd'),
    ('b14C:4152_p', 'cd'),
    ('b14C:4180_p', 'cd'),
    ('b14C:4234_p', 'cd'),
    ('b14C:4248_p', 'cd'),
    ('b14C:4306_p', 'cd'),
    ('b14C:4320_p', 'cd'),
    ('b14C:4378_p', 'cd'),
    ('b14C:4392_p', 'cd'),
    ('b14C:4450_p', 'cd'),
    ('b14C:4464_p', 'cd'),
    ('b14C:4522_p', 'cd'),
    ('b14C:4536_p', 'cd'),
    ('b14C:4590_p', 'cd'),
    ('b14C:4608_p', 'cd'),
    ('b14C:4658_p', 'cd'),
    ('b14C:4676_p', 'cd'),
    ('b14C:4726_p', 'cd'),
    ('b14C:4744_p', 'cd'),
]

# 30
tasks15 = [
    ('b15C:1288_p', 'cd'),
    ('b15C:1306_p', 'cd'),
    ('b15C:1378_p', 'cd'),
    ('b15C:1410_p', 'cd'),
    ('b15C:1430_p', 'cd'),
    ('b15C:1994_p', 'cd'),
    ('b15C:2718_p', 'cd'),
    ('b15C:2726_p', 'cd'),
    ('b15C:2728_n', 'cd'),
    ('b15C:3072_p', 'cd'),
    ('b15C:3284_p', 'cd'),
    ('b15C:4210_n', 'cd'),
    ('b15C:4316_p', 'cd'),
    ('b15C:4750_p', 'cd'),
    ('b15C:4786_n', 'cd'),
    ('b15C:4788_p', 'cd'),
    ('b15C:4796_p', 'cd'),
    ('b15C:4800_n', 'cd'),
    ('b15C:4800_p', 'cd'),
    ('b15C:4808_p', 'cd'),
    ('b15C:4810_n', 'cd'),
    ('b15C:4852_p', 'cd'),
    ('b15C:4854_p', 'cd'),
    ('b15C:4890_n', 'cd'),
    ('b15C:4892_p', 'cd'),
    ('b15C:4900_p', 'cd'),
    ('b15C:4904_n', 'cd'),
    ('b15C:4904_p', 'cd'),
    ('b15C:4912_p', 'cd'),
    ('b15C:4914_n', 'cd'),
]

# 2
tasks17 = [
    ('b17C:49933_n', 'cd'),
    ('b17C:51589_n', 'cd'),
]

# 10
tasks20 = [
    ('b20C:19861_p', 'cd'),
    ('b20C:6355_n', 'cd'),
    ('b20C:6739_p', 'cd'),
    ('b20C:7645_p', 'cd'),
    ('b20C:8857_n', 'cd'),
    ('b20C:8859_n', 'cd'),
    ('b20C:8861_n', 'cd'),
    ('b20C:8863_n', 'cd'),
    ('b20C:8865_n', 'cd'),
    ('b20C:8867_p', 'cd'),
]

# 24
tasks21 = [
    ('b21C:19917_p', 'cd'),
    ('b21C:6921_p', 'cd'),
    ('b21C:6949_p', 'cd'),
    ('b21C:6969_p', 'cd'),
    ('b21C:6997_p', 'cd'),
    ('b21C:7035_p', 'cd'),
    ('b21C:7077_p', 'cd'),
    ('b21C:7131_p', 'cd'),
    ('b21C:7267_p', 'cd'),
    ('b21C:7291_p', 'cd'),
    ('b21C:7317_p', 'cd'),
    ('b21C:7341_p', 'cd'),
    ('b21C:7375_p', 'cd'),
    ('b21C:7403_p', 'cd'),
    ('b21C:7505_p', 'cd'),
    ('b21C:7909_p', 'cd'),
    ('b21C:7937_p', 'cd'),
    ('b21C:8835_n', 'cd'),
    ('b21C:8903_n', 'cd'),
    ('b21C:8905_n', 'cd'),
    ('b21C:8907_n', 'cd'),
    ('b21C:8909_n', 'cd'),
    ('b21C:8911_n', 'cd'),
    ('b21C:8913_p', 'cd'),
]

# 6
tasks22 = [
    ('b22C:18832_p', 'cd'),
    ('b22C:6080_n', 'cd'),
    ('b22C:7800_n', 'cd'),
    ('b22C:7802_n', 'cd'),
    ('b22C:7806_n', 'cd'),
    ('b22C:7808_n', 'cd'),
]

tasks = {
    14: tasks14,
    15: tasks15,
    21: tasks21,
    0: [
        *tasks17,
        *tasks20,
        *tasks22,
    ]
}[args.b]

results = pool.map(worker_function, tasks14)
for result in results:
    print(result)

pool.terminate()
pool.join()
