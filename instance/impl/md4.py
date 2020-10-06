from ..instance import *

ks_st = {
    (40, 128): 6738,
    (48, 96): 7186,
    (48, 128): 8226
}


class MD4(StreamCipher):
    tag = 'md4'

    def __init__(self, steps, size):
        self.type = '%d_%d' % (steps, size)
        self.name = 'Instance: MD4 (%d, %d)' % (steps, size)
        self.path = self.build_path(self.tag, 'md4_%d_%d' % (steps, size))
        super().__init__(
            secret_key=SecretKey(1, size),
            key_stream=KeyStream(ks_st[(steps, size)], 128)
        )


__all__ = [
    'MD4'
]
