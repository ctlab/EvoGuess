class Limit:
    def __init__(self):
        self.limits = {
            'time': 0,
            'restarts': 0,
            'iterations': 1,
            'predictions': 0,
        }

    def set(self, key, value):
        self.limits[key] = value

    def increase(self, key):
        self.limits[key] += 1

    def get(self, key):
        return self.limits[key]

    def exhausted(self) -> bool:
        raise NotImplementedError


__all__ = [
    'Limit'
]
