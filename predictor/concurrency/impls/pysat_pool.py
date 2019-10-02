from ..concurrency import *

from threading import Timer
from time import time as now
from multiprocessing import Pool


def initializer(Solver, cipher):
    global g_solver
    g_solver = Solver(bootstrap_with=cipher.clauses(), use_timer=True)


def solve(task):
    if task.tl > 0:
        timer = Timer(task.tl, g_solver.interrupt, ())
        timer.start()

    timestamp = now()
    status = g_solver.solve_limited(assumptions=task.get())
    time = now() - timestamp

    if task.tl > 0:
        if timer.is_alive():
            timer.cancel()
        else:
            g_solver.clear_interrupt()

    solution = g_solver.get_model() if status else None
    return task.resolve(status, time, solution)


class PySATPool(Concurrency):
    def __init__(self, **kwargs):
        self.pool = None
        super().__init__(**kwargs)

    def initialize(self, solver, **kwargs):
        self.pool = Pool(
            processes=self.processes,
            initializer=initializer,
            initargs=(solver, kwargs['cipher'])
        )
        kwargs['output'].debug(2, 2, "Init pool with %d processes" % self.processes)

    def __solve(self, tasks, **kwargs):
        output = kwargs['output']
        res_list, results = [], []
        for task in tasks:
            res = self.pool.apply_async(solve, (task,))
            res_list.append(res)

        # todo: time limit interruption
        while len(res_list) > 0:
            res_list[0].wait()

            i = 0
            while i < len(res_list):
                if res_list[i].ready():
                    res = res_list.pop(i)
                    if res.successful():
                        results.append(res.get())
                    else:
                        output.debug(0, 1, "Pool solving was completed unsuccessfully")
                else:
                    i += 1

            output.debug(2, 3, "Already solved %d tasks" % len(results))

        self.terminate()
        return results

    def single(self, task: Task, **kwargs) -> Result:
        cipher = kwargs['cipher']
        solver = self.propagator(bootstrap_with=cipher.clauses())
        status = solver.solve(assumptions=task.get())
        solution = solver.get_model() if status else None
        solver.delete()

        return task.resolve(status, 0.1, solution)

    def propagate(self, tasks: List[Task], **kwargs) -> List[Result]:
        self.initialize(self.propagator, **kwargs)
        return self.__solve(tasks, **kwargs)

    def solve(self, tasks: List[Task], **kwargs) -> List[Result]:
        self.initialize(self.solver, **kwargs)
        return self.__solve(tasks, **kwargs)

    def terminate(self):
        if self.pool:
            self.pool.terminate()
            self.pool = None


__all__ = [
    'PySATPool'
]
