class Limit:
    name = 'Limit'

    def __init__(self):
        self.limits = {
            'time': 0,
            'restarts': 0,
            'iterations': 1,
            'predictions': 0,
        }

    def increase(self, key, value=1):
        self.limits[key] += value

    def set(self, key, value):
        self.limits[key] = value

    def get(self, key):
        return self.limits[key]

    def exhausted(self) -> bool:
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Limit'
]
