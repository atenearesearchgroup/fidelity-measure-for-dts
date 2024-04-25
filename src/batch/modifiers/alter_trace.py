import random
from abc import abstractmethod, ABC


class AlterTraceAlignmentWraper(ABC):

    def __init__(self, seed: int = 333):
        self._set_random_seed(seed)

    def _set_random_seed(self, seed: int):
        random.seed(seed)

    @abstractmethod
    def alter_trace(self, execution, config):
        pass
