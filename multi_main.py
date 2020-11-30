import argparse
import random
from concurrent.futures.thread import ThreadPoolExecutor
from os.path import join
from time import sleep

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

    # seeds
    concurrency_seed, method_seed = 3665729543, 4294967295
    # m_seed, c_seed, s_seed = 4294967295, 4294967295, 4294967295

    # instance
    _instance = instance.get_instance(args.instance)
    assert _instance.check(), "Cnf is missing: %s" % _instance.path

    # output
    outputs = []
    alg_count, futures = 4, []

    path = ['output', '_%s_logs' % args.output, _instance.tag, _instance.type]
    for i in range(alg_count):
        outputs.append(
            output.Output(
                dverb=args.verbosity,
                path=join(*[f for f in path if f is not None]),
            ).open().touch()
        )
        sleep(1.0)

    _concurrency = concurrency.MPIExecutor(
        workload=0,
        output=outputs[0],
        random_seed=concurrency_seed,
    )

    executor = ThreadPoolExecutor(max_workers=alg_count)
    for i in range(alg_count):
        _method = method.Method(
            output=outputs[i],
            random_seed=random.randrange(4294967295),
            concurrency=_concurrency,
            sampling=method.sampling.Epsilon(5000, 20000, 5000, 0.1),
            function=method.function.GuessAndDetermine(
                instance=_instance,
                solver=method.solver.pysat.get(args.solver),
                measure=method.function.measure.get(args.measure),
            )
        )

        Algorithm, alg_kwargs = algorithm.get_algorithm(args.algorithm)
        _algorithm = Algorithm(
            **alg_kwargs,
            output=outputs[i],
            method=_method,
            limit=algorithm.limit.WallTime(args.walltime),
            mutation=algorithm.evolution.mutation.Doer(seed=random.randrange(4294967295)),
            selection=algorithm.evolution.selection.Best(seed=random.randrange(4294967295)),
            crossover=algorithm.evolution.crossover.Uniform(prob=0.2, seed=random.randrange(4294967295)),
        )

        backdoor = _instance.secret_key.to_backdoor()
        futures.append(executor.submit(_algorithm.start, backdoor))

    i_points = []
    for i, future in enumerate(futures):
        points = None
        try:
            points = future.result()
        finally:
            i_points.append((i, points))

    for i, points in i_points:
        print(i)
        if points is not None:
            map(print, points)
        else:
            print(None)

    for _output in outputs:
        _output.close()
