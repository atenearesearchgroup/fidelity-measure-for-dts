"""
ndw.constant_gap
~~~~~~~~~~~~~~~~

Class for performing sequence alignment using the Needleman-Wunsch algorithm with constant
gap penalties.
"""

from abc import ABC

import numpy as np
from numba import jit

import util.float_util as fu
from algorithm.ndw.base import NeedlemanWunschBase


class NeedlemanWunschConstantGap(NeedlemanWunschBase, ABC):
    """
    Class for performing sequence alignment using the Needleman-Wunsch algorithm with constant gap
    penalties.

    The Needleman-Wunsch algorithm is a dynamic programming algorithm used to globally align
    two sequences. This class extends algorithm to enable the alignment of not only characters
    but any type of snapshot, which is a list of attributes.

    References:
        - Needleman, S.B., and Wunsch, C.D. (1970). A general method applicable to the search for
          similarities in the amino acid sequence of two proteins. Journal of Molecular Biology,
          48(3), 443-453.
    """

    def calculate_matrix(self) -> np.ndarray:
        """
        Calculates the values of the Dynamic Programming Matrix and stores them in self._table.

        Coding for the matrix
        deletion : 0
        insertion : 1
        mismatch : 2
        match : 3
        """
        _initialize_matrix(self._table, self._continue_gap)

        for i in range(1, self._table.shape[0]):  # + 1
            for j in range(1, self._table.shape[1]):
                equals_value = self._system.snap_equals(self._dt_trace[i - 1],
                                                        self._pt_trace[j - 1],
                                                        self._keys,
                                                        self._mad,
                                                        self._timestamp_label,
                                                        self._low)

                sub = self._table[i - 1, j - 1, 1] + equals_value  # Match/Mismatch
                ins = self._table[i, j - 1, 1] + self._continue_gap  # Insertion
                dele = self._table[i - 1, j, 1] + self._continue_gap  # Deletion

                max_value, max_index = fu.max_tolerance(sub, ins, dele, equals_value)

                self._table[i, j, 1] = max_value
                self._table[i, j, 0] = max_index
                # Match : 3 / Mismatch : 2 / Insertion : 1 / Deletion : 0

        return self._table


@jit(nopython=True)
def _initialize_matrix(table: np.array, continue_gap: float) -> np.ndarray:
    """
    Calculates the values of the Dynamic Programming Matrix and stores them in self._table.

    Coding for the matrix
    deletion : 0
    insertion : 1
    mismatch : 2
    match : 3
    """
    dt_index, pt_index, _ = table.shape

    # table[0, 0, 0] = 0  # Initialization first cell
    # table[0, 0, 1] = 0

    for j in range(1, pt_index):  # + 1
        table[0, j, 0] = 1  # Insertion
        table[0, j, 1] = table[0, j - 1, 1] + continue_gap

    for i in range(1, dt_index):  # + 1
        # table[i, 0, 0] = 0  # Deletion
        table[i, 0, 1] = table[i - 1, 0, 1] + continue_gap
