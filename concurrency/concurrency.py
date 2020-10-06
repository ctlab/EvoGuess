from typing import Iterable, Tuple, Any, Callable

Result = Iterable[Any]
Info = Tuple[int, Iterable[int]]
Task = Tuple[Callable, Iterable[Any]]


class Concurrency:
    name = "Concurrency"

    def __init__(self, output):
        self.output = output

    def submit(self, *tasks: Task) -> int:
        raise NotImplementedError

    def cancel(self, job_id: int) -> bool:
        raise NotImplementedError

    def wait(self, timeout: float) -> Info:
        raise NotImplementedError

    def get(self, job_id: int) -> Result:
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Info',
    'Task',
    'Result',
    'Concurrency'
]

if __name__ == '__main__':
    e = TimeoutError()
    print(type(e).__name__)
