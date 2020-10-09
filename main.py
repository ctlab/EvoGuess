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

    parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')

    args, _ = parser.parse_known_args()

    _instance = instance.get_instance(args.instance)
    assert _instance.check(), "Cnf is missing: %s" % _instance.path

    path = ['output', '_%s_logs' % args.output, _instance.tag, _instance.type]
    _output = output.Output(
        dverb=args.verbosity,
        path=join(*[dr for dr in path if dr is not None]),
    ).open().touch()

    _concurrency = concurrency.MPIExecutor(
        workload=0,
        output=_output,
    )

    random_state = RandomState()
    _method = method.Method(
        output=_output,
        concurrency=_concurrency,
        random_state=random_state,
        sampling=method.sampling.Const(50),
        function=method.function.GuessAndDetermine(
            instance=_instance,
            solver=method.solver.Glucose3(),
            measure=method.function.measure.Propagations(),
        ),
    )

    _algorithm = algorithm.evolution.MuPlusLambda(
        mu=1, lmbda=1,
        output=_output,
        method=_method,
        limit=algorithm.limit.WallTime('00:10:00'),
        mutation=algorithm.evolution.mutation.Uniform(),
        selection=algorithm.evolution.selection.Best(),
    )

    backdoor = _instance.secret_key.to_backdoor()
    points = _algorithm.start(backdoor)

    for point in points:
        print(point)

    _output.close()
