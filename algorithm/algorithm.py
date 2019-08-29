

class Algorithm:
    name = None

    def __init__(self, **kwargs):
        self.comparator = kwargs["comparator"]
        self.condition = kwargs["condition"]

    def start(self, backdoor, **env):
        raise NotImplementedError

    def get_info(self):
        return "-- algorithm: %s\n" % self.name

    def print_iteration_header(self, it, s=""):
        self.out.log("------------------------------------------------------\n",
                        "iteration step: %d%s\n" % (it, " (%s)" % s if len(s) > 0 else ""))

    def print_pf_log(self, hashed, key, value, pf_log):
        self.out.d_log("------------------------------------------------------\n")
        if hashed:
            if pf_log == "":
                self.out.log("hashed backdoor: %s\n" % key,
                                "with value: %.7g\n" % value)
            else:
                self.out.log("update prediction with backdoor: %s\n" % key,
                                pf_log, "end prediction with value: %.7g\n" % value)
        else:
            self.out.log("start prediction with backdoor: %s\n" % key,
                            pf_log, "end prediction with value: %.7g\n" % value)

    def print_local_info(self, local):
        print("------------------------------------------------------")
        print("local with backdoor: %s" % local[0])
        print("and value: %.7g" % local[1])
