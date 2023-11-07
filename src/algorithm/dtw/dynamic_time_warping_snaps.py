import numpy as np
import pandas as pd

from algorithm.dtw.dynamic_time_warping_base import DynamicTimeWarpingBase
from systems import SystemBase
from util.float_util import min_tolerance


class DynamicTimeWarpingSnaps(DynamicTimeWarpingBase):
    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 system: SystemBase,
                 timestamp_label: str = 'timestamp(s)'):
        super().__init__(dt_trace, pt_trace)
        self._timestamp_label = timestamp_label
        self._system = system
        # Table meaning: {diagonal : 1, i-1 : 2, j-1 : 3}
        self._decisions = np.zeros((self._n_dt_trace, self._m_pt_trace))

    def calculate_matrix(self):
        # Table initialization
        for i in range(self._n_dt_trace):
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

            elif pt_size == 0:
                rows.insert(0, self._create_row(dt_size, pt_size - 1, keys))
                dt_size -= 1
                continue

            else:
                # Table meaning: {diagonal : 1, i-1 : 2, j-1 : 3}
                if self._decisions[dt_size][pt_size] == 1:  # diagonal
                    rows.insert(0, self._create_row(dt_size - 1, pt_size - 1, keys))
                    dt_size -= 1
                    pt_size -= 1
                    continue
                elif self._decisions[dt_size][pt_size] == 2:  # i-1
                    rows.insert(0, self._create_row(dt_size - 1, pt_size, keys))
                    dt_size -= 1
                    continue
                elif self._decisions[dt_size][pt_size] == 3:  # j-1
                    rows.insert(0, self._create_row(dt_size, pt_size - 1, keys))
                    pt_size -= 1
                    continue

        return pd.DataFrame(rows, columns=headers)

    def _create_row(self, dt_index, pt_index, keys):
        aux = []
        row = []
        print(f"{dt_index},{pt_index}")
        for key in keys:
            row.append(self._dt_trace[dt_index][key])
            aux.append(self._pt_trace[pt_index][key])

        row.extend(aux)
        return row

    def calculate_alignment(self) -> pd.DataFrame:
        self.calculate_matrix()
        return self._build_result()
