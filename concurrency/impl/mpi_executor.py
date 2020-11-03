from ..concurrency import *
from ..model.job import *

from mpi4py import MPI
from time import time as now, sleep
from mpi4py.futures import ProcessPoolExecutor


class MPIExecutor(Concurrency):
    name = "Concurrency: MPIExecutor"

    def __init__(self, output, **kwargs):
        self.jobs = {}
        self.counter = 0
        self.tick = kwargs.get('tick', 0.1)
        self.workload = kwargs.get('workload', 0.9)
        self.debug_ticks = kwargs.get('debug_ticks', 100)

        super().__init__(output)
        self.mpi_size = MPI.COMM_WORLD.Get_size()
        self.executor = ProcessPoolExecutor(self.mpi_size - 1)

    def submit(self, *tasks: Task) -> int:
        if len(tasks) == 0:
            return None

        self.counter += 1
        job_id = self.counter
        assert job_id not in self.jobs

        futures = []
        for task in tasks:
            future = self.executor.submit(task[0], *task[1:])
            futures.append(future)

        self.jobs[job_id] = Job(futures)
        return job_id

    def cancel(self, job_id: int) -> bool:
        try:
            job = self.jobs.pop(job_id)
            return job.cancel()
        except KeyError:
            return None

    def _update_jobs(self, debug=False):
        ready, all_left = [], 0
        for job_id, job in self.jobs.items():
            job_left = job.update()
            all_left += job_left
            if job_left == 0:
                ready.append(job_id)

        if debug:
            self.output.debug(3, 1, 'Left %d task(s) of %d job(s)' % (all_left, len(self.jobs)))
        return ready, float(all_left) / self.mpi_size

    def wait(self, timeout: float = None) -> Info:
        if timeout is None:
            wall_time = float('inf')
        else:
            wall_time = now() + max(timeout, self.tick)

        i, (ready, loading) = 0, self._update_jobs()
        while wall_time > now():
            if len(ready) > 0 or loading < self.workload:
                break

            sleep(self.tick)
            i = (i + 1) % self.debug_ticks
            ready, loading = self._update_jobs(debug=(i == 0))

        return loading, ready

    def get(self, job_id: int) -> Result:
        if job_id not in self.jobs:
            raise KeyError

        job = self.jobs.pop(job_id)
        try:
            result, exceptions = job.result()
            for i, e in exceptions:
                self.output.error(self.name, 'Exception from job %d of task %d' % (job_id, i), e)

            return result
        except TimeoutError:
            self.jobs[job_id] = job
            return None
        except CancelledError:
            raise KeyError

    def shutdown(self, wait=True):
        self.executor.shutdown(wait)

    def __len__(self):
        return self.mpi_size - 1

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            '-- Tick: %d' % self.tick,
            '-- Workload: %d' % self.workload,
            '-- MPI size: %d' % self.mpi_size,
        ]))


__all__ = [
    'MPIExecutor'
]
