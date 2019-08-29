import argparse

from numpy import concatenate
from numpy.random import randint, RandomState

from predictor.method.map import get_method
from predictor.solver.map import get_solver
from predictor.concurrency.map import get_concurrency
from predictor.key_generator.map import get_algorithm
from predictor.util.case_generator import CaseGenerator
from predictor.util.environment import environment as env


class Gate:
    def __init__(self, **kwargs):
        env.solvers = {}
        env.out = kwargs['output']
        env.algorithm = get_algorithm(kwargs['keygen'])
        env.concurrency = get_concurrency(kwargs['method'])

        for setts in kwargs['solvers']:
            env.solvers[setts['tag']] = get_solver(setts)

        f = get_method(kwargs['method'])
        self.compute = f.compute
        self.calculate = f.calculate

        from mpi4py import MPI
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()

        seeds = randint(2 ** 32 - 1, size=self.size) if self.rank == 0 else []
        seed = self.comm.bcast(seeds, root=0)[self.rank]
        env.case_generator = CaseGenerator(rs=RandomState(seed))

    def predict(self, backdoor, count, **kwargs):
        mpi_count, remainder = divmod(count, self.size)
        mpi_count += 1 if remainder > self.rank else 0

        mpi_cases, time = self.compute(backdoor, [], mpi_count, **kwargs)
        cases, value = self.comm.gather(mpi_cases, root=0), 0

        if self.rank == 0:
            env.out.debug(2, 1, "been gathered cases from %d nodes" % len(cases))
            cases = concatenate(cases)

            value, log, cases = self.calculate(backdoor, (cases, time))
            env.out.log(log)

        return value, time


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EvoGuess')
    parser.add_argument('keygen', type=str, help='key generator')
    parser.add_argument('bds', type=str, help='backdoor\'s file')
    parser.add_argument('-c', '--conf', metavar='json', type=str, default="{}", help='configuration')

    args = parser.parse_args()
