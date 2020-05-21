from math import log

from ..stat_test import *

from scipy.stats import mannwhitneyu


class MannWhitneyu(StatTest):
    name = "StatTest: Mann-Whitneyu"

    def test(self, x: RankCases, y: RankCases):
        nx = self.get_samples(x.cases, x.tl, [x.c, y.c])
        ny = self.get_samples(y.cases, y.tl, [y.c, x.c])

        ylx = self.save_mw_call(nx, ny, 'less')
        xly = self.save_mw_call(ny, nx, 'less')

        return ylx, xly

    def save_mw_call(self, x, y, alternative):
        try:
            return mannwhitneyu(x, y, alternative=alternative).pvalue
        except Exception:
            return 1.

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
