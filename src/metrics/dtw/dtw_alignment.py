import numpy as np

from metrics.alignment_base import AlignmentBase


class DynamicTimeWarpingAlignmentMetrics(AlignmentBase):

    @property
    def score(self) -> float:
        return self._score

    @property
    def percentage_one_to_many(self):
        params = [prefix + self._timestamp_label for prefix in [self.PREFIX_PT, self.PREFIX_PT]]
        n_values = 0
        for p in params:
            n_values += self._alignment[p].value_counts().index.nunique()
        return n_values / np.max([len(self._dt_trace), len(self._pt_trace)])
