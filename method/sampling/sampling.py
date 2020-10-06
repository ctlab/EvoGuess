from instance.model import Backdoor


class Sampling:
    name = 'Sampling'

    def get_count(self, backdoor: Backdoor, sample=()):
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Backdoor',
    'Sampling'
]
