from .impls.comma import *
from .impls.plus import *
from .impls.elitism import *


def get(name):
    return {
        '+': Plus,
        ',': Comma,
        '^': Elitism
    }[name]
