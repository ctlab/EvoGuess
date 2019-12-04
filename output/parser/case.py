from algorithm.models import Individual


class Case(Individual):
    def __init__(self, backdoor, results, cpu_time=-1):
        self.results = results
        self.cpu_time = cpu_time
        super().__init__(backdoor)

    def br(self):
        return self.backdoor, self.results

    def bv(self):
        return self.backdoor, self.value

    def bvr(self):
        return self.backdoor, self.value, self.results

    def get_statistic(self):
        ind = sum([result.status is None for result in self.results])
        return {
            'IND': ind,
            'DET': len(self.results) - ind
        }


__all__ = [
    'Case'
]
