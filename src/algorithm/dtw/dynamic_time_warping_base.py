from abc import ABC, abstractmethod

import numpy as np

from algorithm.alignment_algorithm import AlignmentAlgorithm


class DynamicTimeWarpingBase(ABC, AlignmentAlgorithm):
    def __init__(self, dt_trace: list,
                 pt_trace: list):
        self._dt_trace = dt_trace
        self._pt_trace = pt_trace

        self._n_dt_trace = len(dt_trace) + 1
        self._m_pt_trace = len(pt_trace) + 1

        self._table = np.zeros((self._n_dt_trace, self._m_pt_trace))

    @abstractmethod
    def calculate_matrix(self):
        pass

    @property
    def score(self):
        return self._table[-1, -1]
