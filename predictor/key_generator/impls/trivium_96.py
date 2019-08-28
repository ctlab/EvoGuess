from ..key_generator import StreamCipher


class Trivium_96(StreamCipher):
    key_stream_start = 530
    key_stream_len = 100

    secret_key_start = 1
    secret_key_len = 96

    name = "Trivium 96"
    tag = "trivium_96"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_tr_96 = Trivium_96(self.cnf)
        copy_tr_96.substitutions = self.substitutions

        return copy_tr_96
