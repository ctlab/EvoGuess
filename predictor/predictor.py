from .instance.models.var import Backdoor


class Predictor:
    name = 'Predictor'

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.output = kwargs['output']

        try:
            from mpi4py import MPI
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.Get_rank()
            self.size = self.comm.Get_size()
        except ModuleNotFoundError:
            self.rank, self.size = 0, 1

    def predict(self, backdoor: Backdoor, **kwargs) -> int:
        raise NotImplementedError

    def log_info(self, cases, estimation, time):
        for case in cases:
            self.output.log(str(case))

        self.output.log(str(estimation))
        self.output.log('Spent time: %.2f s' % time)

    def __str__(self):
        return '\n'.join(map(str, [
            self.name,
            self.kwargs['instance'],
        ]))


__all__ = [
    'Backdoor',
    'Predictor',
]
