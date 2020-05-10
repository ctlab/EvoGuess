from ..instance import *


class Curcuit_c6288(Instance):
    tag = 'c6288'

    def __init__(self, param):
        self.name = 'Instance: Curcuit c6288 %d' % param
        self.path = './templates/Curcuit/iscas85/c6288/c6288mut%dn.cnf' % param
        super().__init__(secret_key=SecretKey(1, 32))


__all__ = [
    'Curcuit_c6288'
]
