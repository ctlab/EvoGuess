from ..key_generator import StreamCipher


class Bivium(StreamCipher):
    key_stream_start = 443
    key_stream_len = 200

    secret_key_start = 1
    secret_key_len = 177

    name = "Bivium"
    tag = "bivium"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_bivium = Bivium(self.cnf)
        copy_bivium.substitutions = self.substitutions

        return copy_bivium
