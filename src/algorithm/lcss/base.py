"""
lcss.base
~~~~~~~~~~~~~~~~

Abstract class for the implementation of the Longest Common Subsequence algorithm variants.
"""
from abc import abstractmethod, ABC

import numpy as np
import pandas as pd

from algorithm.ialgorithm import IAlignmentAlgorithm


class LongestCommonSubsequenceBase(ABC, IAlignmentAlgorithm):
    """
    LongestCommonSubsequenceBase is an abstract class that implements the base behavior of the
    Longest Common Subsequence (LCS) algorithm [1].

    The longest common subsequence (LCS) is the longest subsequence common to all sequences in a set
    of sequences (often just two sequences).

    References:
        [1] David Maier (1978). "The Complexity of Some Problems on Subsequences and
        Supersequences". J. ACM. ACM Press. 25 (2): 322–336
    """

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
        """
        Calculates the values of the Dynamic Programming Matrix and stores them in self._table.
        """
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
        """
        Calculate the alignment between two sequences or data sets and return the alignment result
        :return: a DataFrame that includes the alignment
        """
        self.calculate_matrix()
        return pd.DataFrame()

    @property
    def score(self) -> float:
        """
        The resulting score of the algorithm, i.e., the length of the Longest Common Subsequence
        between the traces.
        """
        return self._table[-1][-1] if self._table.size > 0 else 0

    @abstractmethod
    def equals_condition(self, dt_snap, pt_snap) -> bool:
        """
        Returns whether the snapshots dt_snap and pt_snap are equal or not.
        """
