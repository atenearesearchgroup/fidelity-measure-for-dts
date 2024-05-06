import random
from abc import abstractmethod, ABC


class AlterTraceAlignmentWraper(ABC):

    def __init__(self, class_key: str):
        self.key = class_key

    def _set_random_seed(self, seed: int = 333):
        random.seed(seed)

    def alter_trace(self, execution, config):
        self._set_random_seed()
        len_modification = self._remove_key(execution, self.len_key)
        pos_modification = self._remove_key(execution, self.pos_key)

        position, result = self._alter_trace(len_modification, execution, config, pos_modification)

        end, start = self._get_boundaries_ts(config, execution, len_modification, position)
        execution.dt_trace = result

        return {self.key[:4]: f'({start},{end})'}

    def _remove_key(self, execution, key):
        if key in execution.alg_current_config:
            result = execution.alg_current_config[key]
            execution.alg_current_config.pop(key)
            return result
        return -1

    def _get_boundaries_ts(self, config, execution, len_modification, position):
        start = execution.dt_trace[config.timestamp_label][position]
        end = execution.dt_trace[config.timestamp_label][position + len_modification]
        return end, start

    @abstractmethod
    def _alter_trace(self, len_modification, execution, config, pos_modification):
        pass

    @property
    def len_key(self):
        return f'{self.key}_len'

    @property
    def pos_key(self):
        return f'{self.key}_pos'
