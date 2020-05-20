from .concurrency import *

from threading import Timer
from time import time as now


def incr_init(Solver, instance):
    global g_solver
    g_solver = Solver(bootstrap_with=instance.clauses(), use_timer=True)


def base_init(Solver, instance):
    global g_clauses, g_solver
    g_clauses = instance.clauses()
    g_solver = Solver


def incr_solve(task):
    if task.tl > 0:
        timer = Timer(task.tl, g_solver.interrupt, ())
        timer.start()

        timestamp = now()
        status = g_solver.solve_limited(assumptions=task.get())
        time = now() - timestamp

        if timer.is_alive():
            timer.cancel()
        else:
            g_solver.clear_interrupt()
    else:
        timestamp = now()
        status = g_solver.solve(assumptions=task.get())
        time = max(now() - timestamp, g_solver.time())

    solution = g_solver.get_model() if status else None
    return task.resolve(status, time, solution)


def base_solve(task):
    solver = g_solver(bootstrap_with=g_clauses, use_timer=True)

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
        timestamp = now()
        status = solver.solve(assumptions=task.get())
        time = max(now() - timestamp, solver.time())

    solution = solver.get_model() if status else None
    solver.delete()
    return task.resolve(status, time, solution)


class PySAT(Concurrency):
    name = 'PySAT Concurrency'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.incr = kwargs.get('incremental', False)
        self.init_func = incr_init if self.incr else base_init
        self.solve_func = incr_solve if self.incr else base_solve

    def initialize(self, solver, **kwargs):
        raise NotImplementedError

    def single(self, task: Task, **kwargs) -> Result:
        cipher = kwargs['instance']
        solver = self.solver(bootstrap_with=cipher.clauses())
        timestamp = now()
        status = solver.solve(assumptions=task.get())
        time = now() - timestamp
        solution = solver.get_model() if status else None
        solver.delete()

        return task.resolve(status, time, solution)

    def process(self, tasks: List[Task], **kwargs) -> List[Result]:
        raise NotImplementedError

    def propagate(self, tasks: List[Task], **kwargs) -> List[Result]:
        self.initialize(self.propagator, **kwargs)
        return self.process(tasks, **kwargs)

    def solve(self, tasks: List[Task], **kwargs) -> List[Result]:
        self.initialize(self.solver, **kwargs)
        return self.process(tasks, **kwargs)

    def terminate(self):
        raise NotImplementedError

    def __str__(self):
        return '\n'.join(map(str, [
            super().__str__(),
            'Incremental: %s' % self.incr,
        ]))


__all__ = [
    'List',
    'Task',
    'Result',
    'PySAT'
]
