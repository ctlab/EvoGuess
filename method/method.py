from typing import Tuple, Dict, Iterable

from method.function.types import Function
from method.sampling.types import Sampling
from numpy.random.mtrand import RandomState

from structure.array import Backdoor
from structure.data.backdoor_cache import BackdoorCache

Estimation = Dict[str, float]


def number_to_bits(number, size):
    return [1 if number & (1 << (size - 1 - i)) else 0 for i in range(size)]


class Method:
    name = 'Method'

    def __init__(self,
                 output,
                 function: Function,
                 sampling: Sampling,
                 concurrency,
                 random_state: RandomState
                 ):
        self.output = output
        self.sampling = sampling
        self.function = function
        self.concurrency = concurrency
        self.random_state = random_state

        self._active_jobs = {}
        self._permutation_cache = {}
        self._backdoor_cache = BackdoorCache(output)

    def _queue(self, backdoor, task_count, offset):
        bd_key, bd_size = str(backdoor), len(backdoor)
        # generate task_dimension for current backdoor
        # todo: use self.sampling.get_max()
        if bd_size > 20:
            task_dimension = self.random_state.randint(2, size=(task_count, bd_size))
        else:
            if bd_key in self._permutation_cache:
                task_permutation = self._permutation_cache[bd_key]
            else:
                task_permutation = self.random_state.permutation(2 ** bd_size)
                self._permutation_cache[bd_key] = task_permutation

            task_numbers = task_permutation[offset:offset + task_count]
            task_dimension = [number_to_bits(number, bd_size) for number in task_numbers]

        # create new job for current backdoor with task_dimension
        tasks = self.function.get_tasks(backdoor, *task_dimension, random_state=self.random_state)
        job_id = self.concurrency.submit(*tasks)
        self._active_jobs[job_id] = backdoor

        return job_id

    def queue(self, backdoor: Backdoor) -> Tuple[int, Estimation]:
        # check if job with current backdoor already exist
        bd_key = str(backdoor)
        for job_id, job_backdoor in self._active_jobs.items():
            if bd_key == str(job_backdoor):
                return -job_id, None

        # check if backdoor already estimated
        if backdoor in self._backdoor_cache:
            task_sample, estimation = self._backdoor_cache[backdoor]
            values = self.function.get_values(*task_sample)
            task_count = self.sampling.get_count(backdoor, values=values)

            if task_count == 0:
                return None, {**estimation, 'job_time': 0.}
        else:
            task_count, task_sample = self.sampling.get_count(backdoor), []
            if task_count == 0:
                raise Exception("Sample size for new backdoor can't be zero!")

        return self._queue(backdoor, task_count, len(task_sample)), None

    def _handle_job(self, job_id):
        assert job_id in self._active_jobs
        backdoor = self._active_jobs.pop(job_id)

        task_sample, _ = self._backdoor_cache.get(backdoor, ([], {}))
        task_sample += self.concurrency.get(job_id)

        values = self.function.get_values(*task_sample)
        task_count = self.sampling.get_count(backdoor, values=values)
        if task_count > 0:
            self._backdoor_cache[backdoor] = task_sample, None
            self._queue(backdoor, task_count, len(task_sample))
            return backdoor, None

        task_sample = [task for task in task_sample if task is not None]
        statistic, estimation = self.function.calculate(backdoor, *task_sample)

        self._backdoor_cache[backdoor] = task_sample, estimation
        self._backdoor_cache.finalize(backdoor)
        return backdoor, estimation

    def wait(self, timeout=None) -> Tuple[bool, Iterable[Tuple[Backdoor, Estimation]]]:
        while True:
            requeue, estimations = False, []
            loading, completed_jobs = self.concurrency.wait(timeout)
            for job_id in completed_jobs:
                backdoor, estimation = self._handle_job(job_id)
                if estimation is not None:
                    estimations.append((backdoor, estimation))
                else:
                    requeue = True

            if len(estimations) > 0 or not requeue:
                break

        return loading < 1., estimations

    def __len__(self):
        return len(self.concurrency)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.function,
            self.sampling,
            '--------------------',
            self.concurrency,
        ]))


__all__ = [
    'Method',
    'Backdoor',
]
