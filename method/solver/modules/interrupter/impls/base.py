from ..interrupter import *


class Base(Interrupter):
    def hang(self, args: ArgsBuilder) -> ArgsBuilder:
        return args.limit(self.tl)


__all__ = [
    'Base'
]
