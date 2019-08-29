from output.output import Output
from output.builder import CellBuilder as Cell
from algorithm.builder import AlgorithmBuilder as Algorithm


def to_seconds(s):
    time_scale = [1, 60, 60, 24]
    time_units = s.split(':')[::-1]

    if len(time_units) > len(time_scale):
        time_units = time_units[:len(time_scale)]

    time, acc = 0, 1
    for i in range(len(time_units)):
        acc *= time_scale[i]
        time += int(time_units[i]) * acc

    return time


__all__ = [
    'Cell',
    'Output',
    'Algorithm',
    # utils
    'to_seconds',
]
