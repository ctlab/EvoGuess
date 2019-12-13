from threading import Timer

from ...pysat import *

from pebble import ProcessPool


class PebbleMap(PySAT):
    name = 'PySAT Concurrency: PebbleMap'

    def __init__(self, **kwargs):
        self.pool = None
        super().__init__(**kwargs)

    def initialize(self, solver, **kwargs):
        self.pool = ProcessPool(
            max_workers=self.processes,
            initializer=self.init_func,
            initargs=(solver, kwargs['instance'])
        )
        kwargs['output'].debug(2, 2, 'Init pool with %d processes' % self.processes)

    def process(self, tasks: List[Task], **kwargs) -> List[Result]:
        output = kwargs['output']
        results = []
        future = self.pool.map(self.solve_func, tasks)

        # timer = Timer(20., future.cancel, ())
        # timer.start()
        try:
            for result in future.result():
                results.append(result)
                output.debug(2, 3, 'Already solved %d tasks' % len(results))
        except Exception as e:
            output.debug(0, 1, 'Error while fetching pool results: %s' % e)

        # if timer.is_alive():
        #     timer.cancel()

        self.terminate()
        return results

    def terminate(self):
        if self.pool:
            self.pool.stop()
            self.pool.join()
            self.pool = None


__all__ = [
    'PebbleMap'
]
