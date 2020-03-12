from .instance.models.var import Backdoor


class Method:
    name = 'Method'

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.output = kwargs['output']
        self.concurrency = kwargs['concurrency']

        try:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.Get_rank()
            self.size = self.comm.Get_size()
        except ModuleNotFoundError:
            self.rank, self.size = 0, 1

    def run(self, backdoor: Backdoor, **kwargs) -> int:
        raise NotImplementedError

    def estimate(self, backdoor: Backdoor, **kwargs) -> int:
        return self.run(backdoor, **kwargs)

    def log_info(self, cases, output, time):
        for case in cases:
            self.output.log(str(case))

        self.output.log(str(output))
        self.output.log('Spent time: %.2f s' % time)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.concurrency,
            self.kwargs['instance'],
        ]))


__all__ = [
    'Backdoor',
    'Method',
]
