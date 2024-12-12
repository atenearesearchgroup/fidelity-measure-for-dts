import os
from abc import abstractmethod, ABC

import pandas as pd


class WindowStatAnalysis(ABC):
    PERIOD = 'pe'
    DURATION = 'du'
    FD = 'frechet_euclidean'
    ED = 'p2p_mean_euclidean_mean'
    P_MS = 'percentage_matched_snapshots'
    MIN_MS = 'min_per_ms'
    MAX_MS = 'max_per_ms'
    MEAN_MS = 'mean_per_ms'
    STD_MS = 'std_per_ms'

    def __init__(self, modifier, values, path, filename):
        self._values = values
        self.modifier = modifier
        self._metrics = pd.read_csv(os.path.join(path, filename))

    @abstractmethod
    def get_statistics(self, metrics: pd.DataFrame):
        pass

    @abstractmethod
    def calculate_statistics(self, filename: str, result: pd.DataFrame):
        pass

    def _append_statistics(self, result: pd.DataFrame, metrics: pd.DataFrame):
        return pd.concat([result,
                          pd.DataFrame.from_records(
                              [self.get_statistics(metrics)])],
                         ignore_index=True)

    @property
    def values(self):
        return self._values

    @property
    def metrics(self):
        return self._metrics

    @property
    def _modifier_len(self):
        return f'{self.modifier[:2]}_len'

    @property
    def _modifier_pos(self):
        return f'{self.modifier[:2]}_pos'
