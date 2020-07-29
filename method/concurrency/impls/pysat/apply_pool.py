from ...pysat import *

from multiprocessing import Pool


class ApplyPool(PySAT):
    name = 'PySAT Concurrency: ApplyPool'

    def __init__(self, **kwargs):
        self.pool = None
        super().__init__(**kwargs)

    def initialize(self, solver, **kwargs):
        if self.pool is not None:
            kwargs['output'].debug(2, 2, 'Pool already inited')
        else:
            self.pool = Pool(
                processes=self.processes,
                initializer=self.init_func,
                initargs=(solver, kwargs['instance'])
            )
            kwargs['output'].debug(2, 2, 'Init pool with %d processes' % self.processes)

    def process(self, tasks: List[Task], **kwargs) -> List[Result]:
        output = kwargs['output']
        res_list, results = [], []
        for task in tasks:
            res = self.pool.apply_async(self.solve_func, (task,))
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
                        output.debug(0, 1, 'Pool solving was completed unsuccessfully')
                else:
                    i += 1

            output.debug(2, 3, 'Already solved %d tasks' % len(results))

        if not self.keep:
            self.terminate()
        return [result.set_value(self.measure.get(result)) for result in results]

    def terminate(self):
        if self.pool:
            self.pool.terminate()
            self.pool.join()
            self.pool = None


__all__ = [
    'ApplyPool'
]
