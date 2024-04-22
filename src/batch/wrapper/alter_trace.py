import random
from abc import abstractmethod, ABC

from batch.mode.imode import AlignmentMode


class AlterTraceAlignmentWraper(AlignmentMode, ABC):

    def __init__(self, mode: AlignmentMode):
        self.__class__ = type(mode.__class__.__name__,
                              (self.__class__, mode.__class__),
                              {})
        self.__dict__ = mode.__dict__

    def _set_random_seed(self, seed: int = 333):
        random.seed(seed)

    def execute_inner_alignments(self):
        self._execution.dt_trace, position = self._alter_trace(self._execution.alg_current_config,
                                                               self._scenario.dt_trace,
                                                               self._config.params)
        self._execution.params_dict.update(position)
        self.execute_inner_alignments()

    @abstractmethod
    def _alter_trace(self, current_config, trace, params=None):
        pass
