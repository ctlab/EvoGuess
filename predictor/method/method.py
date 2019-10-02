from .models import Estimation
from ..concurrency.models import Result
from ..cipher.models.var import Backdoor

from typing import List, Tuple, Dict


class Method:
    type = None
    name = 'Method'

    def __init__(self, **kwargs):
        self.chunk_size = kwargs['chunk_size']
        self.concurrency = kwargs['concurrency']

    def compute(self, backdoor: Backdoor, cases: List[Result], count: int, **kwargs) -> List[Result]:
        raise NotImplementedError

    def estimate(self, backdoor: Backdoor, cases: List[Result], **kwargs) -> Estimation:
        raise NotImplementedError

    @staticmethod
    def _count(results: List[Result]) -> Dict[str, int]:
        ind = sum([result.status is None for result in results])
        return {
            'IND': ind,
            'DET': len(results) - ind
        }


__all__ = [
    'List',
    'Tuple',
    'Result',
    'Method',
    'Backdoor',
    'Estimation'
]
