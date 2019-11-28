from ..corrector import *
from typing import List, Tuple
from predictor.concurrency.models import Result


class Ruler(Corrector):
    name = 'Corrector: Ruler'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.limiter = kwargs.get("limiter", 0.1)

    def correct(self, results: List[Result], tl: int) -> Tuple[int, int]:
        det_times, ind_times = [], []
        for result in results:
            if result.status is None:
                ind_times.append(tl)
            else:
                det_times.append(result.time)

        if len(det_times) == 0:
            return tl, 0

        det_times.sort()
        k = max(1, round(self.limiter * len(results)))
        if len(det_times) <= k:
            best_tl = det_times[-1]
        else:
            min_tl = max(self.min_tl, det_times[k - 1])
            best_tl = self.choose_best_tl(min_tl, det_times, ind_times)

        dis_count = sum([time > best_tl for time in det_times])
        return best_tl, dis_count


__all__ = [
    'Ruler'
]
