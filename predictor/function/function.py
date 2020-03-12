from .models import Output
from ..concurrency.models import Result
from ..instance.models.var import Backdoor

from typing import List, Dict


class Function:
    type = None
    name = 'Function'

    def __init__(self, **kwargs):
        self.chunk_size = kwargs['chunk_size']

    def evaluate(self, backdoor: Backdoor, cases: List[Result], count: int, **kwargs) -> List[Result]:
        raise NotImplementedError

    def calculate(self, backdoor: Backdoor, cases: List[Result], **kwargs) -> Output:
        raise NotImplementedError

    @staticmethod
    def _count(results: List[Result]) -> Dict[str, int]:
        ind = sum([result.status is None for result in results])
        return {
            'IND': ind,
            'DET': len(results) - ind
        }

    def __str__(self):
        return self.name


__all__ = [
    'List',
    'Output',
    'Result',
    'Function',
    'Backdoor',
]
