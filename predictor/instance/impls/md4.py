from ..instance import *

ks_bits = {
    40: {
        128: (6738, 128)
    },
    48: {
        96: (7186, 128),
        128: (8226, 128)
    }
}


class MD4(StreamCipher):
    tag = 'md4'

    def __init__(self, steps, size):
        self.name = 'Instance: MD4 %d %d' % (steps, size)
        self.path = './templates/MD4/MD4_%d_%d.cnf' % (steps, size)
        super().__init__(
            secret_key=SecretKey(1, size),
            key_stream=KeyStream(*ks_bits[steps][size])
        )


__all__ = [
    'MD4'
]
