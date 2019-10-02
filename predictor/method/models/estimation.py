class Estimation:
    def __init__(self, value, statistic={}):
        self.value = value
        self.statistic = statistic

    def __str__(self):
        return str(self.statistic).replace('\'', '')


__all__ = [
    'Estimation'
]
