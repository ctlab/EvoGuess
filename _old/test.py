import argparse

from numpy.random.mtrand import RandomState
from pysat.solvers import Cadical, Glucose3

from algorithm.models import Individual
from method import *
from algorithm import *
from method.concurrency import VerticalPySAT
from method.concurrency.models import Task
from method.instance.models.var import Backdoor
from output import Cell

parser = argparse.ArgumentParser(description='Test')
parser.add_argument('-t', '--threads', metavar='4', type=int, default=4, help='concurrency threads')

args, _ = parser.parse_known_args()

solver = Glucose3
inst = instance.get('a5')
backdoor = inst.secret_key.to_backdoor()
backdoor = backdoor.get_copy([True] * 30)
# backdoor = Backdoor.parse('2..10 20..30 39 40 42..52')

pool = VerticalPySAT(
    solver=solver,
    propagator=solver,
    threads=args.threads,
    instance=inst
)

cell = Cell(
    path=['output', '_rrr', inst.tag],
    largs={},
    dargs={
        'verb': 3
    },
).open(description='').touch()

count = 8
rs = RandomState()
init_sols = []
for i in range(count):
    init = pool.single(Task(i, proof=True, secret_key=inst.secret_key.values(rs=rs)), instance=inst)
    init_sols.append(init.solution)

print(backdoor)
tasks = [Task((i, i), tl=10, backdoor=backdoor.values(solution=init_sols[i]), **inst.values(init_sols[i])) for i
         in range(count)]

results = pool.solve(tasks, output=cell)
for result in results:
    print(result.i[1], result)
print(sum(r.time for r in results))

mut = mutation.Doer()
for _ in range(3):
    ind = mut.mutate(Individual(backdoor))
    backdoor = ind.backdoor

    print(backdoor)
    tasks = [Task((i, i), tl=10, backdoor=backdoor.values(solution=init_sols[i]), **inst.values(init_sols[i])) for i in
             range(count)]

    results = pool.solve(tasks, output=cell)
    for result in results:
        print(result.i[1], result)
    print(sum(r.time for r in results))


backdoor = backdoor.get_copy([])
print(backdoor)
tasks = [Task((i, i), tl=10, backdoor=backdoor.values(solution=init_sols[i]), **inst.values(init_sols[i])) for i
         in range(count)]

results = pool.solve(tasks, output=cell)
for result in results:
    print(result.i[1], result)
print(sum(r.time for r in results))

pool.terminate()
cell.close()

