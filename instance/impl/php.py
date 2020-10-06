from ..instance import *


class PHP(Instance):
    tag = 'php'

    def __init__(self, p, h):
        self.type = '%d_%d' % (p, h)
        self.name = 'Instance: PHP (%d pigeons, %d holes)' % (p, h)
        self.path = self.build_path(self.tag, 'php-%d-%d' % (p, h))
        super().__init__(secret_key=SecretKey(1, p * h))


__all__ = [
    'PHP'
]
