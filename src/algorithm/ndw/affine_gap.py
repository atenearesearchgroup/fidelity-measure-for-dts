"""
ndw.affine_gap
~~~~~~~~~~~~~~~~

Class for performing sequence alignment using the Needleman-Wunsch algorithm with affine
gap penalties.
"""
from abc import ABC

import numpy as np

from algorithm.ndw.base import NeedlemanWunschBase
from systems.system import SystemBase
from util.float_util import max_tolerance


class NeedlemanWunschAffineGap(NeedlemanWunschBase, ABC):
    """
    Class for performing sequence alignment using the Needleman-Wunsch algorithm with affine
    gap penalties.

    The Needleman-Wunsch algorithm is a dynamic programming algorithm used to globally align
    two sequences. This class extends the algorithm to incorporate affine gap penalties, where
    gap opening and gap extension penalties can be different.

    This version includes the alignment of not only characters but any type of snapshot, which
    is a list of attributes.

    References:
        - Needleman, S.B., and Wunsch, C.D. (1970). A general method applicable to the search for
          similarities in the amino acid sequence of two proteins. Journal of Molecular Biology,
          48(3), 443-453.
    """
    MIN = -float("inf")

    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 system: SystemBase,
                 timestamp_label: str = "timestamp(s)",
                 init_gap: float = -0.2,
                 cont_gap: float = 0,
                 mad: dict = None,
                 low: int = 5):
        super().__init__(dt_trace, pt_trace, system, timestamp_label,
                         init_gap=init_gap, mad=mad)
        self._continue_gap = cont_gap
        self._low = low

        # Dynamic programming tables
        # +1 to consider the alignment with the empty string
        self._insert_table = np.zeros((len(dt_trace) + 1, len(pt_trace) + 1, 1))
        self._deletion_table = np.zeros((len(dt_trace) + 1, len(pt_trace) + 1, 1))

    def _init_deletion(self, i, j):
        """
        Returns the score that corresponds to cells of the first row and column of
        the deletion table
        """
        if i > 0 and j == 0:
            return self.MIN
        if j > 0:
            return self._init_gap + (self._continue_gap * j)
        return 0

    def _init_insertion(self, i, j):
        """
        Returns the score that corresponds to cells of the first row and column of
        the insertion table
        """
        if j > 0 and i == 0:
            return self.MIN
        if i > 0:
            return self._init_gap + (self._continue_gap * i)
        return 0

    def _init_match(self, i, j):
        """
        Initializes a cell of the table that tracks the matched pairs of the alignment.
        It is used to initialize the first row and column of this table.
        """
        # if j == 0 and i == 0:
        #   self._table[i, j, 0] = 0
        #   self._table[i, j, 1] = 0 # Deletion
        # else:
        if j == 0 and not i == 0:
            # self._table[i, j, 0] = 0  # Deletion
            self._table[i, j, 1] = self._init_gap + (self._continue_gap * i)
        elif i == 0 and not j == 0:
            self._table[i, j, 0] = 1  # Insertion
            self._table[i, j, 1] = self._init_gap + (self._continue_gap * j)

    def calculate_matrix(self) -> np.ndarray:
        """
        Calculates the values of the Dynamic Programming Matrix and stores them in self._table.

        Coding for the matrix
        deletion : 0
        insertion : 1
        mismatch : 2
        match : 3
        """
        dt_index, pt_index, _ = self._table.shape

        for j in range(0, pt_index):
            for i in range(0, dt_index):
                self._init_match(i, j)

        self._deletion_table = np.array(
            [[self._init_deletion(i, j) for j in range(0, pt_index)] for i in range(0, dt_index)])
        self._insert_table = np.array(
            [[self._init_insertion(i, j) for j in range(0, pt_index)] for i in range(0, dt_index)])

        for j in range(1, pt_index):
            for i in range(1, dt_index):
                self._deletion_table[i][j] = \
                    max((self._init_gap + self._continue_gap + self._table[i - 1][j][1]),
                        (self._continue_gap + self._deletion_table[i - 1][j]), )
                self._insert_table[i][j] = \
                    max((self._init_gap + self._continue_gap + self._table[i][j - 1][1]),
                        (self._continue_gap + self._insert_table[i][j - 1]))

                equals_value = self._system.snap_equals(self._dt_trace[i - 1],
                                                        self._pt_trace[j - 1],
                                                        self._mad,
                                                        self._timestamp_label,
                                                        self._low)

                sub = self._table[i - 1, j - 1, 1] + equals_value

                max_value, max_index = max_tolerance(sub,
                                                     self._insert_table[i][j],
                                                     self._deletion_table[i][j],
                                                     equals_value)

                self._table[i, j, 1] = max_value
                self._table[i, j, 0] = max_index
                # Match : 3 / Mismatch : 2 / Insertion : 1 / Deletion : 0

        return self._table
