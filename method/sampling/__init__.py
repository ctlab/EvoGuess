from .impl import *

impls = [
    Const,
    Epsilon,
]


def get_sampling(_instance, params):
    for _impl in impls:
        kwargs = _impl.parse(params)
        if kwargs is not None:
            return _impl(_instance, **kwargs)


__all__ = [
    'get_sampling'
]
