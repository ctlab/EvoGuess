from ..instance import *


class Circuit_b14C(Instance):
    tag = 'b14C'

    def __init__(self, bit, c):
        self.name = 'Instance: Circuit b14C %d %s' % (bit, c)
        self.path = './templates/Circuit/itc99/b14_C/b14_Cmut%d%s.cnf' % (bit, c)
        super().__init__(secret_key=SecretKey(1, 277))


class Circuit_b15C(Instance):
    tag = 'b15C'

    def __init__(self, bit, c):
        self.name = 'Instance: Circuit b15C %d %s' % (bit, c)
        self.path = './templates/Circuit/itc99/b15/b15_Cmut%d%s.cnf' % (bit, c)
        super().__init__(secret_key=SecretKey(1, 485))


class Circuit_b17C(Instance):
    tag = 'b17C'

    def __init__(self, bit, c):
        self.name = 'Instance: Circuit b17C %d %s' % (bit, c)
        self.path = './templates/Circuit/itc99/b17/b17_Cmut%d%s.cnf' % (bit, c)
        super().__init__(secret_key=SecretKey(1, 1452))


class Circuit_b20C(Instance):
    tag = 'b20C'

    def __init__(self, bit, c):
        self.name = 'Instance: Circuit b20C %d %s' % (bit, c)
        self.path = './templates/Circuit/itc99/b20/b20_Cmut%d%s.cnf' % (bit, c)
        super().__init__(secret_key=SecretKey(1, 522))


class Circuit_b21C(Instance):
    tag = 'b21C'

    def __init__(self, bit, c):
        self.name = 'Instance: Circuit b21C %d %s' % (bit, c)
        self.path = './templates/Circuit/itc99/b21/b21_Cmut%d%s.cnf' % (bit, c)
        super().__init__(secret_key=SecretKey(1, 522))


class Circuit_b22C(Instance):
    tag = 'b22C'

    def __init__(self, bit, c):
        self.name = 'Instance: Circuit b22C %d %s' % (bit, c)
        self.path = './templates/Circuit/itc99/b22/b22_Cmut%d%s.cnf' % (bit, c)
        super().__init__(secret_key=SecretKey(1, 767))


class Circuit_c6288(Instance):
    tag = 'c6288'

    def __init__(self, param):
        self.name = 'Instance: Circuit c6288 %d' % param
        self.path = './templates/Circuit/iscas85/c6288/c6288mut%dn.cnf' % param
        super().__init__(secret_key=SecretKey(1, 32))


__all__ = [
    'Circuit_b14C',
    'Circuit_b15C',
    'Circuit_b17C',
    'Circuit_b20C',
    'Circuit_b21C',
    'Circuit_b22C',
    'Circuit_c6288',
]
