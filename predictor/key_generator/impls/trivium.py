from ..key_generator import StreamCipher


class Trivium(StreamCipher):
    key_stream_start = 1588
    key_stream_len = 300

    secret_key_start = 1
    secret_key_len = 288

    name = "Trivium"
    tag = "trivium"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_tr = Trivium(self.cnf)
        copy_tr.substitutions = self.substitutions

        return copy_tr
