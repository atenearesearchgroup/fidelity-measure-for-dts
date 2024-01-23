"""
dtw.base
~~~~~~~~~~~~~~~~

Abstract class for the implementation of the Dynamic Time Warping variants.
"""

from abc import ABC, abstractmethod

import numpy as np

from algorithm.ialgorithm import IAlignmentAlgorithm


class DynamicTimeWarpingBase(ABC, IAlignmentAlgorithm):
    """
    Abstract class that implements the basic structure for Dynamic Time Warping (DTW).

    Dynamic Time Warping is a technique used for measuring the similarity between two sequences
    that may vary in time or speed.

    References:
        - Olsen, NL; Markussen, B; Raket, LL (2018), "Simultaneous inference for misaligned
        multivariate functional data", Journal of the Royal Statistical Society, Series C,
        67 (5): 1147–76
    """

    def __init__(self, dt_trace: dict,
                 pt_trace: dict):
        self._dt_trace = dt_trace
        self._pt_trace = pt_trace

        self._n_dt_trace = len(dt_trace) + 1
        self._m_pt_trace = len(pt_trace) + 1

        self._table = np.zeros((self._n_dt_trace, self._m_pt_trace))

    @abstractmethod
    def calculate_matrix(self):
        """
        Calculates the values of the Dynamic Programming Matrix and stores them in self._table.
        """

    @property
    def score(self):
        """
        The resulting score of the algorithm, i.e., the closest distance between the traces
        according to DTW.
        """
        return self._table[-1, -1]
