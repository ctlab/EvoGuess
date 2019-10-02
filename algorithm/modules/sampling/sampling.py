class Sampling:
    name = "Sampling"

    def __len__(self):
        raise NotImplementedError

    def __str__(self):
        return self.name


__all__ = [
    'Sampling'
]
