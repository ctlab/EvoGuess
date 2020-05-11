from ..concurrency import *

from threading import Timer
from time import time as now
from pebble import ProcessPool
from multiprocessing import Process, Queue


def propagate_init(Solver, instance):
    global g_solver
    g_solver = Solver(bootstrap_with=instance.clauses(), use_timer=True)


def propagate_solve(task):
    status = g_solver.solve(assumptions=task.get())
    time = g_solver.time()
    solution = g_solver.get_model() if status else None
    return task.resolve(status, time, solution)


def worker_process(queue, chunk):
    for solver, task in chunk:
        if task.tl > 0:
            timer = Timer(task.tl, solver.interrupt, ())
            timer.start()

            timestamp = now()
            status = solver.solve_limited(assumptions=task.get())
            time = now() - timestamp

            if timer.is_alive():
                timer.cancel()
            else:
                solver.clear_interrupt()
        else:
            status = solver.solve(assumptions=task.get())
            time = solver.time()

        solution = solver.get_model() if status else None
        queue.put(task.resolve(status, time, solution))


class MyPool(Concurrency):
    name = 'Vertical PySAT Concurrency: MyPool'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.solvers = {}

    def single(self, task: Task, **kwargs) -> Result:
        cipher = kwargs['instance']
        solver = self.solver(bootstrap_with=cipher.clauses(), use_timer=True)
        status = solver.solve(assumptions=task.get())
        time = solver.time()
        solution = solver.get_model() if status else None
        solver.delete()

        return task.resolve(status, time, solution)

    def propagate(self, tasks: List[Task], **kwargs) -> List[Result]:
        output, instance = kwargs['output'], kwargs['instance']

        self.terminate()
        pool = ProcessPool(
            max_workers=self.processes,
            initializer=propagate_init,
            initargs=(self.propagator, instance)
        )
        results = []
        future = pool.map(propagate_solve, tasks)
        try:
            for result in future.result():
                results.append(result)
                output.debug(2, 3, 'Already solved %d tasks' % len(results))
        except Exception as e:
            output.debug(0, 1, 'Error while fetching pool results: %s' % e)
        pool.stop()
        pool.join()

        return results

    def solve(self, tasks: List[Task], **kwargs) -> List[Result]:
        output, instance = kwargs['output'], kwargs['instance']

        clauses, args = instance.clauses(), []
        for task in tasks:
            key = str(task.i)
            if key in self.solvers:
                solver = self.solvers.get(key)
                # output.debug(2, 2, '%s In bits: %s' % (key, task.get(in_bits=False)))
            else:
                # cnf = clauses + [[a] for a in task.get(in_bits=False)]
                # output.debug(2, 2, '%s In bits: %s' % (key, task.get(in_bits=False)))
                solver = self.solver(bootstrap_with=clauses, use_timer=True)
                self.solvers[key] = solver
                output.debug(2, 2, 'Init solver with key: %s' % key)

            args.append((solver, task))

        processes, queue, st = [], Queue(), 0
        chunksize, remainder = divmod(len(args), self.processes)
        for i in range(self.processes):
            length = chunksize + (1 if remainder > i else 0)
            chunk = args[st:st + length]
            process = Process(target=worker_process, args=(queue, chunk))
            processes.append(process)
            process.start()
            st += length

        results = []
        while len(results) < len(tasks):
            results.append(queue.get())

        results = sorted(results, key=lambda r: r.i[1])
        return results

    def terminate(self):
        for solver in self.solvers.values():
            solver.delete()

        self.solvers = {}


__all__ = [
    'MyPool'
]
