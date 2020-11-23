import argparse
from os.path import join

from numpy.random.mtrand import RandomState

import output
import method
import instance
import algorithm
import concurrency

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EvoGuess v2')
    parser.add_argument('instance', type=str, help='instance of problem')
    parser.add_argument('-o', '--output', metavar='str', type=str, default='main', help='output subdir')
    parser.add_argument('-v', '--verbosity', metavar='3', type=int, default=3, help='debug [0-3] verbosity level')
    parser.add_argument('-wt', '--walltime', metavar='hh:mm:ss', type=str, default='24:00:00', help='wall time')
    parser.add_argument('-a', '--algorithm', metavar='str', type=str, default='1+1', help='optimization algorithm')

    parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
    parser.add_argument('-m', '--measure', metavar='str', type=str, default='props', help='measure of estimation')

    args, _ = parser.parse_known_args()

    _instance = instance.get_instance(args.instance)
    assert _instance.check(), "Cnf is missing: %s" % _instance.path

    path = ['output', '_%s_logs' % args.output, _instance.tag, _instance.type]
    _output = output.Output(
        dverb=args.verbosity,
        path=join(*[f for f in path if f is not None]),
    ).open().touch()

    random_state = RandomState()
    _concurrency = concurrency.MPIExecutor(
        workload=0,
        output=_output,
        random_state=random_state,
    )

    _method = method.Method(
        output=_output,
        concurrency=_concurrency,
        random_state=random_state,
        sampling=method.sampling.Epsilon(50, 200, 50, 0.1),
        function=method.function.GuessAndDetermine(
            instance=_instance,
            solver=method.solver.pysat.get(args.solver),
            measure=method.function.measure.get(args.measure),
        )
    )
    Algorithm, alg_kwargs = algorithm.get_algorithm(args.algorithm)
    _algorithm = Algorithm(
        **alg_kwargs,
        output=_output,
        method=_method,
        limit=algorithm.limit.WallTime(args.walltime),
        mutation=algorithm.evolution.mutation.Doer(),
        selection=algorithm.evolution.selection.Best(),
        crossover=algorithm.evolution.crossover.Uniform(prob=0.2),
    )

    backdoor = _instance.secret_key.to_backdoor()
    points = _algorithm.start(backdoor)

    for point in points:
        print(point)

    _output.close()
