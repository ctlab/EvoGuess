from ..key_generator import StreamCipher


class Geffe(StreamCipher):
    key_stream_start = 301
    key_stream_len = 100

    secret_key_start = 1
    secret_key_len = 64

    name = "Geffe"
    tag = "geffe"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_geffe = Geffe(self.cnf)
        copy_geffe.substitutions = self.substitutions

        return copy_geffe
