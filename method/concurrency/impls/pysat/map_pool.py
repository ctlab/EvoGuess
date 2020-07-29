from ...pysat import *

from multiprocessing import Pool


class MapPool(PySAT):
    name = 'PySAT Concurrency: MapPool'

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
        results = []
        res = self.pool.map_async(self.solve_func, tasks)

        # todo: time limit interruption
        res.wait()
        if res.ready() and res.successful():
            results = res.get()
        else:
            output.debug(0, 1, 'Pool solving was completed unsuccessfully')

        output.debug(2, 3, 'Pool solved %d tasks' % len(results))

        if not self.keep:
            self.terminate()
        return [result.set_value(self.measure.get(result)) for result in results]

    def terminate(self):
        if self.pool:
            self.pool.terminate()
            self.pool.join()
            self.pool = None


__all__ = [
    'MapPool'
]
