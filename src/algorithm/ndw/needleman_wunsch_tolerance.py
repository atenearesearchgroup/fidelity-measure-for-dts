from abc import ABC

import numpy as np

import util.float_util as fu
from algorithm.ndw.needleman_wunsch_base import NeedlemanWunschBase


class NeedlemanWunschTolerance(NeedlemanWunschBase, ABC):
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
        Coding for the matrix
        deletion : 0
        insertion : 1
        mismatch : 2
        match : 3
        """
        dt_index, pt_index, _ = self._table.shape

        # table[0, 0, 0] = 0  # Initialization first cell
        # table[0, 0, 1] = 0

        for j in range(0, pt_index):  # + 1
            self._table[0, j, 0] = 1  # Insertion
            self._table[0, j, 1] = self._table[0, j - 1, 1] + self._continue_gap

        for i in range(0, dt_index):  # + 1
            # table[i, 0, 0] = 0  # Deletion
            self._table[i, 0, 1] = self._table[i - 1, 0, 1] + self._continue_gap

            for j in range(1, pt_index):
                equals_value = self._system.snap_equals(self._dt_trace[i - 1],
                                                        self._pt_trace[j - 1],
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
