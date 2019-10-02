from ..interrupter import *


class Timelimit(Interrupter):
    def hang(self, args: ArgsBuilder) -> ArgsBuilder:
        if self.tl > 0:
            args.wrap(['timelimit', '-t%d' % self.tl]) \
                .limit(self.tl)

        return args


__all__ = [
    'Timelimit'
]
