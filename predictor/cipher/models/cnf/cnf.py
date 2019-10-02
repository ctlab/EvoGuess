import re

from copy import copy
from _operator import add
from functools import reduce


class Cnf:
    def __init__(self, *clauses):
        self.str = ''
        self.max = 0
        self.clauses = []
        self.edited = True
        self.conjunct(*clauses)

    def conjunct(self, *clauses):
        if not len(clauses): return

        self.max = max(self.max, *map(max, clauses))
        self.clauses.extend(clauses)
        self.edited = True
        return self

    def __update_str(self):
        def ctos(clause):
            return ' '.join(map(str, clause + [0])) + '\n'

        if self.edited:
            self.edited = False
            self.str = reduce(add, map(ctos, self.clauses))

    def to_str(self, *substitutions):
        subs = reduce(add, map(str, substitutions), '')
        length = reduce(add, map(len, substitutions), len(self))
        header = 'p cnf %d %d\n' % (self.max, length)

        self.__update_str()
        return reduce(add, [header, self.str, subs])

    def __len__(self):
        return len(self.clauses)

    def __str__(self):
        return self.to_str()

    def __copy__(self):
        copy_cnf = Cnf()
        copy_cnf.max = self.max
        copy_cnf.str = self.str
        copy_cnf.edited = self.edited
        copy_cnf.clauses = copy(self.clauses)
        return copy_cnf

    @staticmethod
    def parse(path):
        with open(path) as f:
            cnf = Cnf()
            fst = re.compile('^[-0-9]')
            line = f.readline().strip()
            while line:
                if fst.search(line):
                    clause = [int(n) for n in line.split(' ')]
                    if clause[-1] == 0:
                        clause.pop(-1)

                    cnf.conjunct(clause)

                line = f.readline().strip()

            return cnf


class CnfSubstitution:
    def __init__(self, *args):
        self.vars = []
        self.substitute(*args)

    def substitute(self, *args):
        self.vars.extend(args)
        return self

    def __len__(self):
        return len(self.vars)

    def __str__(self):
        return ''.join('%d 0\n' % x for x in self.vars)


__all__ = [
    'Cnf',
    'CnfSubstitution'
]
