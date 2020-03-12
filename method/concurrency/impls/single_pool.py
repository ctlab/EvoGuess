from ..concurrency import *

from multiprocessing.pool import Pool


def initializer(instance, solver):
    global g_cnf, g_solver
    g_cnf = instance.cnf()
    g_solver = solver


def solve(task):
    cnf = g_cnf.to_str(task.get())
    report = g_solver.solve(cnf)

    return task.resolve(report.status, report.time, report.solution)


class SinglePool(Concurrency):
    name = 'Concurrency: SinglePool'

    def __init__(self, **kwargs):
        self.pool = None
        super().__init__(**kwargs)

    def __initialize(self, solver, **kwargs):
        if self.pool is not None:
            kwargs['output'].debug(2, 2, 'Pool already inited')
        else:
            self.pool = Pool(
                processes=self.processes,
                initializer=initializer,
                initargs=(kwargs['instance'], solver)
            )
            kwargs['output'].debug(2, 2, 'Init pool with %d processes' % self.processes)

    def __solve(self, tasks, **kwargs):
        output = kwargs['output']
        res_list, results = [], []
        for task in tasks:
            res = self.pool.apply_async(solve, (task,))
            res_list.append(res)

        while len(res_list) > 0:
            res_list[0].wait()

            i = 0
            while i < len(res_list):
                if res_list[i].ready():
                    res = res_list.pop(i)
                    try:
                        results.append(res.get())
                    except Exception as e:
                        output.debug(0, 1, 'Pool solving was completed unsuccessfully: %s', e)
                else:
                    i += 1

            output.debug(2, 3, 'Already solved %d tasks' % len(results))

        if not self.keep:
            self.terminate()
        return results

    def single(self, task: Task, **kwargs) -> Result:
        cnf = kwargs['instance'].cnf().to_str(task.get())
        report = self.propagator.solve(cnf)

        return task.resolve(report.status, report.time, report.solution)

    def propagate(self, tasks: List[Task], **kwargs) -> List[Result]:
        self.__initialize(self.propagator, **kwargs)
        return self.__solve(tasks, **kwargs)

    def solve(self, tasks: List[Task], **kwargs) -> List[Result]:
        self.__initialize(self.solver, **kwargs)
        return self.__solve(tasks, **kwargs)

    def terminate(self):
        self.pool.terminate()
        self.pool = None


__all__ = [
    'SinglePool'
]
