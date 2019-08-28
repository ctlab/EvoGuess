from ..key_generator import StreamCipher


class Volfram(StreamCipher):
    key_stream_start = 12417
    key_stream_len = 128

    secret_key_start = 1
    secret_key_len = 128

    name = "Volfram"
    tag = "volfram"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_volfram = Volfram(self.cnf)
        copy_volfram.substitutions = self.substitutions

        return copy_volfram
