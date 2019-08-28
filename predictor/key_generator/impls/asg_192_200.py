from ..key_generator import StreamCipher


class ASG_192_200(StreamCipher):
    key_stream_start = 22506
    key_stream_len = 200

    secret_key_start = 1
    secret_key_len = 192

    name = "ASG_192_200"
    tag = "asg_192_200"

    def __init__(self, cnf):
        StreamCipher.__init__(self, cnf)

    def __copy__(self):
        copy_asg = ASG_192_200(self.cnf)
        copy_asg.substitutions = self.substitutions

        return copy_asg
