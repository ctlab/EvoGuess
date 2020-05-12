from ..instance import *


class Curcuit_b14C(Instance):
    tag = 'b14C'

    def __init__(self, param):
        self.name = 'Instance: Curcuit b14C %d' % param
        self.path = './templates/Curcuit/itc99/b14_C/b14_Cmut%dn.cnf' % param
        super().__init__(secret_key=SecretKey(1, 277))


class Curcuit_c6288(Instance):
    tag = 'c6288'

    def __init__(self, param):
        self.name = 'Instance: Curcuit c6288 %d' % param
        self.path = './templates/Curcuit/iscas85/c6288/c6288mut%dn.cnf' % param
        super().__init__(secret_key=SecretKey(1, 32))


__all__ = [
    'Curcuit_b14C',
    'Curcuit_c6288',
]
