"""
dtw.snaps
~~~~~~~~~~~~~~~~

Implementation of Dynamic Time Warping adapted to enable the alignment of snapshot sequences.
"""

import numpy as np
import pandas as pd

from algorithm.dtw.base import DynamicTimeWarpingBase
from systems import SystemBase
from util.float_util import min_tolerance


class DynamicTimeWarpingSnaps(DynamicTimeWarpingBase):
    """
    This class implements the Dynamic Time Warping algorithm [1] adapted to enable the alignment of
    snapshot sequences.

    Dynamic Time Warping is a technique used for measuring the similarity between two sequences
    that may vary in time or speed.

    References:
        [1] Olsen, NL; Markussen, B; Raket, LL (2018), "Simultaneous inference for misaligned
        multivariate functional data", Journal of the Royal Statistical Society, Series C,
        67 (5): 1147–76
    """

    def __init__(self, dt_trace: dict,
                 pt_trace: dict,
                 system: SystemBase,
                 timestamp_label: str = 'timestamp(s)'):
        super().__init__(dt_trace, pt_trace)
        self._timestamp_label = timestamp_label
        self._system = system
        # Table meaning: {diagonal : 1, i-1 : 2, j-1 : 3}
        self._decisions = np.zeros((self._n_dt_trace, self._m_pt_trace))

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
                distance = self._system.distance(self._dt_trace[i - 1],
                                                 self._pt_trace[j - 1],
                                                 self._timestamp_label)
                last_min, decision = min_tolerance(
                    self._table[i - 1, j - 1], self._table[i - 1, j], self._table[i, j - 1])
                self._table[i, j] = distance + last_min
                self._decisions[i, j] = decision

    def _build_result(self):
        """
        Performs backtracking on the Dynamic Programming Matrix to obtain the pairs aligned by
        the algorithm.
        """
        dt_size = len(self._dt_trace) - 1
        pt_size = len(self._pt_trace) - 1
        keys = self._pt_trace[0].keys()
        rows = []

        # Add headers to file
        headers = ["dt-" + k for k in keys]
        headers.extend(["pt-" + k for k in keys])

        while dt_size > 0 or pt_size > 0:
            if dt_size == 0:
                rows.insert(0, self._create_row(dt_size - 1, pt_size, keys))
                pt_size -= 1
                continue
            if pt_size == 0:
                rows.insert(0, self._create_row(dt_size, pt_size - 1, keys))
                dt_size -= 1
                continue

            # Table meaning: {diagonal : 1, i-1 : 2, j-1 : 3}
            if self._decisions[dt_size][pt_size] == 1:  # diagonal
                rows.insert(0, self._create_row(dt_size - 1, pt_size - 1, keys))
                dt_size -= 1
                pt_size -= 1
                continue
            if self._decisions[dt_size][pt_size] == 2:  # i-1
                rows.insert(0, self._create_row(dt_size - 1, pt_size, keys))
                dt_size -= 1
                continue
            if self._decisions[dt_size][pt_size] == 3:  # j-1
                rows.insert(0, self._create_row(dt_size, pt_size - 1, keys))
                pt_size -= 1
                continue

        return pd.DataFrame(rows, columns=headers)

    def _create_row(self, dt_index, pt_index, keys):
        """Returns a list with the DT snapshots attributes followed by those of the PT."""
        aux = []
        row = []
        for key in keys:
            row.append(self._dt_trace[dt_index][key])
            aux.append(self._pt_trace[pt_index][key])

        row.extend(aux)
        return row

    def calculate_alignment(self) -> pd.DataFrame:
        """
        Calculate the alignment between two sequences or data sets and return the alignment result
        :return: a DataFrame that includes the alignment
        """
        self.calculate_matrix()
        return self._build_result()
