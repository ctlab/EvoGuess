class SolverSettings:
    def __init__(self, **kwargs):
        self.settings = {
            "tl_util": False,
            "tl": 0,
            "workers": 1,
            "attempts": 5,
            "simplify": True
        }
        self.update(**kwargs)

    def update(self, **kwargs):
        for key in kwargs.keys():
            self.settings[key] = kwargs[key]

    def get(self, key):
        return self.settings[key]

    def __str__(self):
        return str(self.settings)
