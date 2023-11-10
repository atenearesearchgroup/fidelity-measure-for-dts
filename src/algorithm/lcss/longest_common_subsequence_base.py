from abc import abstractmethod, ABC

import numpy as np
import pandas as pd

from algorithm.alignment_algorithm import AlignmentAlgorithm


class LongestCommonSubsequenceBase(ABC, AlignmentAlgorithm):
    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 param_interest: str):
        self._dt_trace = dt_trace
        self._pt_trace = pt_trace

        self._n_dt_trace = len(dt_trace)
        self._m_pt_trace = len(pt_trace)

        self._param_interest = param_interest

        self._table = np.zeros((self._n_dt_trace, self._m_pt_trace))

    def calculate_matrix(self):
        for i in range(self._n_dt_trace):
            for j in range(self._m_pt_trace):
                if self.equals_condition(self._dt_trace[i], self._pt_trace[j]):
                    if i == 0 or j == 0:
                        self._table[i][j] = 1
                    else:
                        self._table[i][j] = self._table[i - 1][j - 1] + 1
                else:
                    self._table[i][j] = np.max([self._table[i - 1][j], self._table[i][j - 1]])

    def calculate_alignment(self) -> pd.DataFrame:
        self.calculate_matrix()
        return pd.DataFrame()

    @property
    def score(self) -> float:
        return self._table[-1][-1]

    @abstractmethod
    def equals_condition(self, dt_snap, pt_snap) -> bool:
        pass
