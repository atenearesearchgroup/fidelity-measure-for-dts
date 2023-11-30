import numpy as np
import pandas as pd

from algorithm.dtw.dynamic_time_warping_base import DynamicTimeWarpingBase


class DynamicTimeWarpingLugaresi(DynamicTimeWarpingBase):

    def __init__(self, dt_trace: dict,
                 pt_trace: dict,
                 param_interest: str):
        super().__init__(dt_trace, pt_trace)
        self._dt_trace = [x[param_interest] for x in self._dt_trace]
        self._pt_trace = [x[param_interest] for x in self._pt_trace]

    def _normalize_traces(self):
        max_value = max((max(self._dt_trace), max(self._pt_trace)))
        self._dt_trace[:] = [value / max_value for value in self._dt_trace]
        self._pt_trace[:] = [value / max_value for value in self._pt_trace]

    def calculate_matrix(self):
        # Table initialization
        for i in range(self._n_dt_trace):
            for j in range(self._m_pt_trace):
                self._table[i, j] = np.inf
        self._table[0, 0] = 0

        for i in range(1, self._n_dt_trace):
            for j in range(1, self._m_pt_trace):
                distance = abs(self._dt_trace[i - 1] - self._pt_trace[j - 1])
                # np.min is slower than min for small arrays because:
                # - constructs a ndarray from the list
                # - determines that the correct call is minimum.reduce to do the operation
                # - call minimum.reduce (which itself is still much slower than the
                # straight python call)
                # Taken from: https://github.com/numpy/numpy/issues/12350
                last_min = np.min(
                    [self._table[i - 1, j], self._table[i, j - 1], self._table[i - 1, j - 1]])
                self._table[i, j] = distance + last_min

    def calculate_alignment(self) -> pd.DataFrame:
        # Normalize the traces before computing DTW
        self._normalize_traces()
        self.calculate_matrix()
        return pd.DataFrame()
