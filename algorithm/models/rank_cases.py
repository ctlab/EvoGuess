class RankCases:
    def __init__(self, backdoor, tl, cases=()):
        self.tl = tl
        self.backdoor = backdoor
        self.cases = list(cases)
        self.c = 2 ** len(backdoor)

    def __len__(self):
        return len(self.cases)

    def __str__(self):
        s = '['
        for case in self.cases:
            s += '%s, ' % str(case)
        return '%s]' % s[:-2]

    def extend(self, cases):
        self.cases.extend(cases)


__all__ = [
    'RankCases'
]
