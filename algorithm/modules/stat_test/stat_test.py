from algorithm.models.rank_cases import RankCases


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
    'RankCases'
]
