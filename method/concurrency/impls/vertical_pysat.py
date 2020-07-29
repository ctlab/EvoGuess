from ..concurrency import *

import threading
from queue import Empty
from threading import Timer
from pebble import ProcessPool
from time import time as now, sleep
from multiprocessing import Process, Queue

RUN = 0
CLOSE = 1
TERMINATE = 2


def handle_workers(pool):
    thread = threading.current_thread()

    while thread._state != TERMINATE:
        pool.maintain_pool()
        sleep(0.1)


# propagation
def propagate_init(Solver, instance):
    global g_solver
    g_solver = Solver(bootstrap_with=instance.clauses(), use_timer=True)


def propagate_solve(task):
    status = g_solver.solve(assumptions=task.get())
    time = g_solver.time()
    stats = g_solver.accum_stats()
    solution = g_solver.get_model() if status else None
    return task.resolve(status, time, stats, solution)


# solving
def solve_process(in_queue, out_queue, args):
    solvers = {}
    Solver, instance = args
    while True:
        try:
            task = in_queue.get()
        except (EOFError, OSError):
            break

        if task is None:
            break

        key = str(task.i)
        if key in solvers:
            solver = solvers.get(key)
        else:
            solver = Solver(bootstrap_with=instance.clauses(), use_timer=True)
            solvers[key] = solver

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

        stats = solver.accum_stats()
        solution = solver.get_model() if status else None
        out_queue.put(task.resolve(status, time, stats, solution))


class VerticalPySAT(Concurrency):
    name = 'Vertical PySAT Concurrency'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pool = {}
        self.inputs = [Queue() for _ in range(self.processes)]
        self.outputs = [Queue() for _ in range(self.processes)]

        self.instance = kwargs['instance']
        self._worker_handler = threading.Thread(
            target=handle_workers,
            args=(self,)
        )
        self._worker_handler.daemon = True
        self._worker_handler._state = 0
        self._worker_handler.start()

    def single(self, task: Task, **kwargs) -> Result:
        cipher = kwargs['instance']
        solver = self.solver(bootstrap_with=cipher.clauses(), use_timer=True)
        status = solver.solve(assumptions=task.get())
        time = solver.time()
        stats = solver.accum_stats()
        solution = solver.get_model() if status else None
        solver.delete()

        result = task.resolve(status, time, stats, solution)
        return result.set_value(self.measure.get(result))

    def propagate(self, tasks: List[Task], **kwargs) -> List[Result]:
        output, instance = kwargs['output'], kwargs['instance']

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

        return [result.set_value(self.measure.get(result)) for result in results]

    def solve(self, tasks: List[Task], **kwargs) -> List[Result]:
        output = kwargs['output']

        output.debug(2, 2, 'Pool with %d processes ready' % len(self.pool.keys()))
        counter = [0] * self.processes
        for task in tasks:
            i = task.i[1] % self.processes
            self.inputs[i].put(task)
            counter[i] += 1

        results = []
        timestamp, ignore = now(), -1
        while sum(counter) > 0:
            for i in range(self.processes):
                if ignore == i:
                    ignore = -1
                else:
                    if counter[i] > 0:
                        try:
                            result = self.outputs[i].get(timeout=2.)
                            results.append(result)
                            counter[i] -= 1
                        except Empty:
                            ignore = i

            if now() - timestamp > 2:
                timestamp = now()
                output.debug(2, 3, 'Already solved %d tasks' % len(results))

        if now() - timestamp > 2:
            output.debug(2, 3, 'Already solved %d tasks' % len(results))

        results = sorted(results, key=lambda r: r.i[1])
        return [result.set_value(self.measure.get(result)) for result in results]

    def terminate(self):
        self._worker_handler._state = TERMINATE

        if threading.current_thread() is not self._worker_handler:
            self._worker_handler.join()

        for inp in self.inputs:
            inp.put(None)

        for worker in self.pool.values():
            if worker.exitcode is None:
                worker.terminate()

        for worker in self.pool.values():
            if worker.is_alive():
                worker.join()

    def maintain_pool(self):
        if self._join_exited_workers():
            self._repopulate_pool()

    def _join_exited_workers(self):
        cleaned = False
        for i in range(self.processes):
            worker = self.pool.get(i)
            if worker is None:
                cleaned = True
                continue

            if worker.exitcode is not None:
                worker.join()
                cleaned = True
                del self.pool[i]
        return cleaned

    def _repopulate_pool(self):
        for i in range(self.processes):
            if self.pool.get(i) is not None:
                continue

            worker = Process(
                target=solve_process,
                args=(
                    self.inputs[i], self.outputs[i],
                    (self.solver, self.instance)
                )
            )
            self.pool[i] = worker
            worker.daemon = True
            worker.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()


__all__ = [
    'VerticalPySAT'
]
