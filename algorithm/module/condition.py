class Condition:
    def __init__(self, **kwargs):
        self.conditions = {
            'iteration': 1,
            'pf_calls': 0,
            'pf_value': float('inf'),
            'locals': 0,
            'time': 0
        }
        self.key = kwargs['key']
        self.stop = kwargs['stop']

    def set(self, key, value):
        self.conditions[key] = value

    def increase(self, key):
        self.conditions[key] += 1

    def get(self, key=None):
        return self.conditions[key or self.key]

    def check(self):
        return self.stop(self.get())
