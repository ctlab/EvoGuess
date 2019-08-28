from ..key_generator import StreamCipher


class Salsa20(StreamCipher):
    key_stream_start = 26465
    key_stream_len = 512

    secret_key_start = 1
    secret_key_len = 512

    name = "Salsa20"
    tag = "salsa20"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_salsa20 = Salsa20(self.cnf)
        copy_salsa20.substitutions = self.substitutions

        return copy_salsa20
