class Estimation:
    def __init__(self, value, statistic={}, *strs):
        self.strs = strs
        self.value = value
        self.statistic = statistic

    def __str__(self):
        return '\n'.join(map(str, [
            *self.strs,
            self.statistic,
        ])).replace('\'', '')


__all__ = [
    'Estimation'
]
