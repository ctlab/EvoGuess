from ..key_generator import StreamCipher


class E0(StreamCipher):
    key_stream_start = 1785
    key_stream_len = 128

    secret_key_start = 1
    secret_key_len = 128

    name = "E0"
    tag = "e0"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_e0 = E0(self.cnf)
        copy_e0.substitutions = self.substitutions

        return copy_e0
