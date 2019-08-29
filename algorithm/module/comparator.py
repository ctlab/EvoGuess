from numpy import sign, count_nonzero as cnz


class Comparator:
    name = 'comparator'

    def __init__(self, **kwargs):
        pass

    def compare(self, p1, p2):
        raise NotImplementedError

    def __str__(self):
        return self.name


class MaxMin(Comparator):
    # max s, min value
    def compare(self, p1, p2):
        try:
            vs = int(sign(p1[1] - p2[1]))
        except ValueError:
            vs = 0

        return vs if vs != 0 else cnz(p2[0]) - cnz(p1[0])


comparators = {
    'max_min': MaxMin
}
