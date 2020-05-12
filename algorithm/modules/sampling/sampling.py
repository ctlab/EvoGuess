from method.instance.models.var import Backdoor


class Sampling:
    name = 'Sampling'

    def get_size(self, backdoor: Backdoor):
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Backdoor',
    'Sampling'
]
