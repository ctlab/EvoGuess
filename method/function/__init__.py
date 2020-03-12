from .impls import *
from .models import *
from .modules import *
from . import impls, modules


def get(name):
    return {
        'gad': GuessAndDetermine,
        'ibs': InverseBackdoorSets
    }[name]


__all__ = ['get']
__all__.extend(impls.__all__)
__all__.extend(modules.__all__)
