from algorithm.models.rank_cases import RankCases

import numpy as np


def rankdata(a, method='average', *, axis=None):
    if method not in ('average', 'min', 'max', 'dense', 'ordinal'):
        raise ValueError('unknown method "{0}"'.format(method))

    if axis is not None:
        a = np.asarray(a)
        if a.size == 0:
            # The return values of `normalize_axis_index` are ignored.  The
            # call validates `axis`, even though we won't use it.
            # use scipy._lib._util._normalize_axis_index when available
            np.core.multiarray.normalize_axis_index(axis, a.ndim)
            dt = np.float64 if method == 'average' else np.int_
            return np.empty(a.shape, dtype=dt)
        return np.apply_along_axis(rankdata, axis, a, method)

    arr = np.ravel(np.asarray(a))
    alg = 'mergesort' if method == 'ordinal' else 'quicksort'
    sorter = np.argsort(arr, kind=alg)

    inv = np.empty(sorter.size, dtype=np.intp)
    inv[sorter] = np.arange(sorter.size, dtype=np.intp)

    if method == 'ordinal':
        return inv + 1

    arr = arr[sorter]
    obs = np.r_[True, arr[1:] != arr[:-1]]
    dense = obs.cumsum()[inv]

    if method == 'dense':
        return dense

    # cumulative counts of each unique value
    count = np.r_[np.nonzero(obs)[0], len(obs)]

    if method == 'max':
        return count[dense]

    if method == 'min':
        return count[dense - 1] + 1

    # average method
    return .5 * (count[dense] + count[dense - 1] + 1)


def tiecorrect(rankvals):
    arr = np.sort(rankvals)
    idx = np.nonzero(np.r_[True, arr[1:] != arr[:-1], True])[0]
    cnt = np.diff(idx).astype(np.float64)

    size = np.float64(arr.size)
    return 1.0 if size < 2 else 1.0 - (cnt ** 3 - cnt).sum() / (size ** 3 - size)


class StatTest:
    name = "Statistical Test"

    def __init__(self, **kwargs):
        self.bound = kwargs["bound"]
        self.step_size = kwargs["step_size"]

    def test(self, x: RankCases, y: RankCases):
        raise NotImplementedError

    def __str__(self):
        return self.name + ' (%.2f)' % self.bound


__all__ = [
    'StatTest',
    'RankCases',
    'rankdata',
    'tiecorrect'
]
