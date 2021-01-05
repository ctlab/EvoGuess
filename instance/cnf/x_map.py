import pickle

x_maps = {}


class XMAP:
    def __init__(self, data):
        self.data = data

    def get_cnf_var(self, variable, value):
        return self.data['%d-%d' % (variable, value)]

    @staticmethod
    def parse(path, key=None):
        if key is not None and key in x_maps:
            return x_maps[key]

        with open(path, 'rb') as f:
            data = pickle.load(f)
            x_map = XMAP(data)

            if key is not None:
                x_maps[key] = x_map
            return x_map


__all__ = [
    'XMAP'
]
