class Estimation:
    def __init__(self, cases, value):
        self.value = value
        self.cases = cases
        self.from_cache = False

    def __len__(self):
        return len(self.cases)


__all__ = [
    'Estimation'
]
