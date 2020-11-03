import argparse
from os.path import join
from time import time as now
from numpy.random.mtrand import RandomState

from structure.array import Backdoor
from structure.individual import Individual

import output
import method
import instance
import concurrency

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='EvoGuess v2')
    parser.add_argument('instance', type=str, help='instance of problem')
    parser.add_argument('backdoors', type=str, help='load backdoor from specified file')
    parser.add_argument('-o', '--output', metavar='str', type=str, default='check', help='output subdir')
    parser.add_argument('-v', '--verbosity', metavar='3', type=int, default=3, help='debug [0-3] verbosity level')

    parser.add_argument('-s', '--solver', metavar='str', type=str, default='g3', help='SAT-solver to solve')
    parser.add_argument('-m', '--measure', metavar='str', type=str, default='props', help='measure of estimation')

    args, _ = parser.parse_known_args()
    backdoors = Backdoor.load(args.backdoors)

    _instance = instance.get_instance(args.instance)
    assert _instance.check(), "Cnf is missing: %s" % _instance.path

    path = ['output', '_%s_logs' % args.output, _instance.tag, _instance.type]
    _output = output.Output(
        dverb=args.verbosity,
        path=join(*[f for f in path if f is not None]),
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
        sampling=method.sampling.Const(200000),
        function=method.function.GuessAndDetermine(
            instance=_instance,
            solver=method.solver.pysat.get(args.solver),
            measure=method.function.measure.get(args.measure),
        )
    )

    st_timestamp = now()
    _output.info(str(_method))
    for i, backdoor in enumerate(backdoors):
        # todo: queue all backdoor
        i_timestamp = now()
        individual = Individual(backdoor)
        job_id, estimation = _method.queue(backdoor)
        if estimation is None:
            _, estimations = _method.wait()
            estimation = list(estimations)[0]
            assert backdoor == estimation[0]
            estimation = estimation[1]

        _output.log(
            'Iteration %d (stamp: %.2f)' % (i, now() - st_timestamp),
            'Individuals (1):',
            '-- %s' % str(individual.set(**estimation)),
            'Time: %.2f' % (now() - i_timestamp),
            '----------------------------------------'
        )

    _output.close()
