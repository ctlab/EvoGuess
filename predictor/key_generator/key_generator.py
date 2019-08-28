class KeyGenerator:
    key_stream_start = None
    key_stream_len = None

    secret_key_start = None
    secret_key_len = None

    name = None
    tag = None

    short_statuses = {
        None: None,
        "SATISFIABLE": "SAT",
        "UNSATISFIABLE": "UNSAT",
        "INDETERMINATE": "INDET"
    }

    def __init__(self, cnf):
        self.cnf = cnf
        self.substitutions = {}

        self.time = None
        self.status = None
        self.flags = []
        self.solution = []

    def __str__(self):
        return "key generator: %s" % self.name

    def __len__(self):
        return self.key_stream_start + self.key_stream_len - 1

    def substitute(self, **kwargs):
        self.substitutions = kwargs
        return self

    def get_cnf(self):
        return self.cnf.to_str(*self.substitutions.values())

    def write_to(self, file_path):
        with open(file_path, 'w+') as f:
            f.write(self.get_cnf())

    def mark_solved(self, report):
        self.time = report.time
        self.status = report.status
        self.flags = report.flags
        self.solution = report.solution

    def check_solution(self):
        if len(self.solution) == 0:
            raise Exception("Solution is not specified")

        if len(self.solution) != self.__len__():
            raise Exception("Solution not corrected")

    def get_status(self, short=False):
        return self.short_statuses[self.status] if short else self.status

    def get_solution_sk(self):
        if len(self.solution) != self.key_stream_start + self.key_stream_len - 1:
            return []

        start = self.secret_key_start - 1
        end = start + self.secret_key_len
        return self.solution[start:end]

    def get_solution_ks(self):
        if len(self.solution) != self.key_stream_start + self.key_stream_len - 1:
            return []

        start = self.key_stream_start - 1
        end = start + self.key_stream_len
        return self.solution[start:end]


class StreamCipher(KeyGenerator):
    def __init__(self, cnf):
        KeyGenerator.__init__(self, cnf)


class BlockCipher(KeyGenerator):
    public_key_start = None
    public_key_len = None

    def __init__(self, cnf):
        KeyGenerator.__init__(self, cnf)
        self.public_key = None
