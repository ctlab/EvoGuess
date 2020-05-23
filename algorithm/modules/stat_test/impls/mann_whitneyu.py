from ..stat_test import *
from .. import distributions

import numpy as np


class MannWhitneyu(StatTest):
    name = "StatTest: Mann-Whitneyu"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alternative = kwargs.get('alternative', 'less')
        self.use_continuity = kwargs.get('use_continuity', True)

    def mannwhitneyu(self, x, y):
        x, y = np.asarray(x), np.asarray(y)
        n1, n2 = len(x), len(y)
        ranked = rankdata(np.concatenate((x, y)))
        rankx = ranked[0:n1]  # get the x-ranks
        u1 = n1 * n2 + (n1 * (n1 + 1)) / 2.0 - np.sum(rankx, axis=0)  # calc U for x
        u2 = n1 * n2 - u1  # remainder is U for y
        T = tiecorrect(ranked)
        if T == 0: return 1.
        sd = np.sqrt(T * n1 * n2 * (n1 + n2 + 1) / 12.0)

        meanrank = n1 * n2 / 2.0 + 0.5 * self.use_continuity
        if self.alternative == 'less':
            bigu = u1
        elif self.alternative == 'greater':
            bigu = u2
        else:  # two-sided
            bigu = max(u1, u2)

        z = (bigu - meanrank) / sd
        p = distributions.dnorm(-z, 0, 1)
        if self.alternative == 'two-sided':
            p = 2 * p

        u = u2
        # This behavior is deprecated.
        if self.alternative is None:
            u = min(u1, u2)
        return u, p

    def test(self, x: RankCases, y: RankCases):
        nx = self.get_samples(x.cases, x.tl, [x.c, y.c])
        ny = self.get_samples(y.cases, y.tl, [y.c, x.c])

        # ylx = self.save_mw_call(nx, ny, 'less')
        # xly = self.save_mw_call(ny, nx, 'less')

        _, t_ylx = self.mannwhitneyu(nx, ny)
        _, t_xly = self.mannwhitneyu(ny, nx)

        # if ylx < self.bound <= t_ylx:
        #     print('cmp ylx: %.4f vs %.4f' % (ylx, t_ylx))
        # if xly < self.bound <= t_xly:
        #     print('cmp xly: %.4f vs %.4f' % (xly, t_xly))

        return t_ylx, t_xly

    # def save_mw_call(self, x, y, alternative):
    #     try:
    #         return mannwhitneyu(x, y, alternative=alternative).pvalue
    #     except Exception:
    #         return 1.

    def get_samples(self, cases, tl, cs):
        if tl > 0:
            det_times, ind_times = [], []
            for case in cases:
                time = max(0.000001, case.time)
                if case.status is None:
                    ind_times.append(time)
                else:
                    det_times.append(time)

            bound, samples = tl * min(cs), []
            for time in det_times:
                rank = cs[0] * float(time)
                samples.append(rank if rank < bound else bound)

            samples.extend([bound] * len(ind_times))
        else:
            samples = []
            for case in cases:
                time = max(0.000001, case.time)
                samples.append(cs[0] * float(time))

        return samples


__all__ = [
    'MannWhitneyu'
]
