class Case:
    def __init__(self, backdoor, value, results, cpu_time=-1):
        self.value = value
        self.results = results
        self.backdoor = backdoor
        self.cpu_time = cpu_time

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

    def __str__(self):
        return "%.7g for %s" % (self.value, self.backdoor)


__all__ = [
    'Case'
]
