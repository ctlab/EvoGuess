from ..instance import *


class PHP(Instance):
    tag = 'php'

    def __init__(self, p, h):
        self.name = 'Instance: PHP (%d pigeons, %d holes)' % (p, h)
        self.path = './templates/PHP/php-%d-%d.cnf' % (p, h)
        super().__init__(secret_key=SecretKey(1, p * h))


__all__ = [
    'PHP'
]
