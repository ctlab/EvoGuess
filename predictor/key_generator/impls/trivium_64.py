from ..key_generator import StreamCipher


class Trivium_64(StreamCipher):
    key_stream_start = 398
    key_stream_len = 75

    secret_key_start = 1
    secret_key_len = 64

    name = "Trivium 64"
    tag = "trivium_64"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_tr_64 = Trivium_64(self.cnf)
        copy_tr_64.substitutions = self.substitutions

        return copy_tr_64
