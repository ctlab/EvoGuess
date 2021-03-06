from ..instance import *

ks_st = {
    (513, 512): 97938,
}


class Rabbit(StreamCipher):
    base = 2
    tag = 'rabbit'

    def __init__(self, sk, ks):
        self.type = '%d_%d' % (sk, ks)
        self.name = 'Cipher: Rabbit %d/%d' % (sk, ks)
        self.cnf_path = self.build_cnf_path(self.tag, 'rabbit_%d_%d' % (sk, ks))
        super().__init__(
            secret_key=SecretKey(1, sk),
            key_stream=KeyStream(ks_st[(sk, ks)], ks)
        )


__all__ = [
    'Rabbit'
]
