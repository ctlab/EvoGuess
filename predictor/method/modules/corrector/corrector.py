from typing import List, Tuple

from predictor.concurrency.models import Result


class Corrector:
    name = 'Corrector'

    def __init__(self, **kwargs):
        self.min_tl = kwargs.get('min_tl', 0.001)

    def correct(self, results: List[Result], tl: int) -> Tuple[int, int]:
        raise NotImplementedError

    @staticmethod
    def choose_best_tl(bound, det_times, ind_times):
        exactly, perhaps = [], []
        for time in det_times:
            if time <= bound:
                exactly.append(time)
            else:
                perhaps.append(time)

        if len(perhaps) == 0:
            return bound

        perhaps.sort()
        if len(exactly) == 0:
            time = perhaps.pop(0)
            exactly.append(time)

        n = len(det_times) + len(ind_times)
        best = (bound, bound * n / len(exactly))

        for i in range(len(perhaps)):
            value = perhaps[i] * n / (len(exactly) + i + 1)
            if value <= best[1]:
                best = (perhaps[i], value)

        return best[0]

    def __str__(self):
        return self.name


__all__ = [
    'Corrector'
]
