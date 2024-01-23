"""
dtw.lugaresi
~~~~~~~~~~~~~~~~

Implementation of Dynamic Time Warping as presented by Lugaresi et al. in [1].

References:
    [1] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
    Online validation of digital twins for manufacturing systems. Comput.
    Ind. 150: 103942 (2023)
"""

import numpy as np
import pandas as pd

from algorithm.dtw.base import DynamicTimeWarpingBase


class DynamicTimeWarpingLugaresi(DynamicTimeWarpingBase):
    """
    This class implements the Dynamic Time Warping algorithm [1] as implemented in [2] for
    comparison purposes.

    Dynamic Time Warping is a technique used for measuring the similarity between two sequences
    that may vary in time or speed.

    References:
        [1] Olsen, NL; Markussen, B; Raket, LL (2018), "Simultaneous inference for misaligned
        multivariate functional data", Journal of the Royal Statistical Society, Series C,
        67 (5): 1147–76
        [2] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
        Online validation of digital twins for manufacturing systems. Comput.
        Ind. 150: 103942 (2023)
    """

    def __init__(self, dt_trace: dict,
                 pt_trace: dict,
                 param_interest: str):
        super().__init__(dt_trace, pt_trace)
        self._dt_trace = [x[param_interest] for x in self._dt_trace]
        self._pt_trace = [x[param_interest] for x in self._pt_trace]

    def _normalize_traces(self):
        """
        It normalizes the trace values by dividing each value by the maximum value within the
        corresponding trace.
        """
        max_value = max((max(self._dt_trace), max(self._pt_trace)))
        self._dt_trace[:] = [value / max_value for value in self._dt_trace]
        self._pt_trace[:] = [value / max_value for value in self._pt_trace]

    def calculate_matrix(self):
        """
        Calculates the values of the Dynamic Programming Matrix and stores them in self._table.
        """
        for i in range(self._n_dt_trace):  # Table initialization
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
        """
        Calculate the alignment between two sequences or data sets and return the alignment result
        :return: a DataFrame that includes the alignment
        """
        self._normalize_traces()
        self.calculate_matrix()
        return pd.DataFrame()
