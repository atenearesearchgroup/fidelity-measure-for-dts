"""
ndw.affine_gap
~~~~~~~~~~~~~~~~

Class for performing sequence alignment using the Needleman-Wunsch algorithm with affine
gap penalties.
"""
from abc import ABC

import numpy as np
import pandas as pd
from numba import jit

from algorithm.ndw.base import NeedlemanWunschBase
from systems.system import SystemBase
from util.float_util import max_tolerance

MIN = -float("inf")


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

    def __init__(self, dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 system: SystemBase,
                 lca: bool,
                 timestamp_label: str = "timestamp(s)",
                 init_gap: float = -0.2,
                 cont_gap: float = 0,
                 mad: dict = None,
                 low: int = 5):
        super().__init__(dt_trace, pt_trace, system, lca, timestamp_label,
                         init_gap=init_gap, mad=mad, low=low, cont_gap=cont_gap)

        # Dynamic programming tables
        # +1 to consider the alignment with the empty string
        self._insertion_table = np.zeros((len(dt_trace) + 1, len(pt_trace) + 1))
        self._deletion_table = np.zeros((len(dt_trace) + 1, len(pt_trace) + 1))

    def calculate_matrix(self) -> np.ndarray:
        """
        Calculates the values of the Dynamic Programming Matrix and stores them in self._table.

        The dynamic programming matrix is filled based on the following coding:
        - Deletion: 0
        - Insertion: 1
        - Mismatch: 2
        - Match: 3

        :return: The calculated dynamic programming matrix.
        :rtype: np.ndarray
        """
        _initialize_matrices(self._table, self._deletion_table, self._insertion_table,
                             self._init_gap, self._continue_gap)

        for i in range(1, self._table.shape[0]):
            for j in range(1, self._table.shape[1]):
                self._deletion_table[i, j] = \
                    max((self._init_gap + self._continue_gap + self._table[i - 1, j, 1]),
                        (self._continue_gap + self._deletion_table[i - 1, j]))
                self._insertion_table[i, j] = \
                    max((self._init_gap + self._continue_gap + self._table[i, j - 1, 1]),
                        (self._continue_gap + self._insertion_table[i, j - 1]))

                equals_value = self._system.snap_equals(self._dt_trace[i - 1],
                                                        self._pt_trace[j - 1],
                                                        self._mad,
                                                        self._types,
                                                        self._timestamp_range,
                                                        self._dt_low[i - 1],
                                                        self._pt_low[j - 1],
                                                        self._low)

                sub = self._table[i - 1, j - 1, 1] + equals_value

                max_value, max_index = max_tolerance(sub,
                                                     self._insertion_table[i][j],
                                                     self._deletion_table[i][j],
                                                     equals_value)

                self._table[i, j, 1] = max_value
                self._table[i, j, 0] = max_index
                # Match : 3 / Mismatch : 2 / Insertion : 1 / Deletion : 0

        return self._table


@jit(nopython=True)
def _init_deletion(table: np.array, init_gap: float, continue_gap: float, i: int, j: int):
    """
    Initializes the score for cells of the first row and column of the deletion table.

    This function calculates and assigns the score for the specified cell position
    in the deletion table. If the cell corresponds to the first row (i.e., i > 0 and j == 0),
    it assigns negative infinity (-∞) as the score. If the cell corresponds to the first column
    (i.e., j > 0), it calculates the score based on the initialization gap penalty and the
    continuation gap penalty multiplied by the column index. Otherwise, it assigns 0 as the score.

    :param table: The deletion table to initialize.
    :type table: np.array
    :param init_gap: Penalty for initiating a gap sequence in the alignment.
    :type init_gap: float
    :param continue_gap: Penalty for continuing a gap sequence in the alignment.
    :type continue_gap: float
    :param i: The row index of the cell.
    :type i: int
    :param j: The column index of the cell.
    :type j: int
    """
    if i > 0 and j == 0:
        table[i, j] = -np.inf
    elif j > 0:
        table[i, j] = init_gap + (continue_gap * j)
    else:
        table[i, j] = 0


@jit(nopython=True)
def _init_insertion(table: np.array, init_gap: float, continue_gap: float, i: int, j: int):
    """
    Initializes the score for cells of the first row and column of the insertion table.

    This function calculates and assigns the score for the specified cell position
    in the insertion table. If the cell corresponds to the first column (i.e., j > 0 and i == 0),
    it assigns negative infinity (-∞) as the score. If the cell corresponds to the first row
    (i.e., i > 0), it calculates the score based on the initialization gap penalty and the
    continuation gap penalty multiplied by the row index. Otherwise, it assigns 0 as the score.

    :param table: The insertion table to initialize.
    :type table: np.array
    :param init_gap: Penalty for initiating a gap sequence in the alignment.
    :type init_gap: float
    :param continue_gap: Penalty for continuing a gap sequence in the alignment.
    :type continue_gap: float
    :param i: The row index of the cell.
    :type i: int
    :param j: The column index of the cell.
    :type j: int
    """
    if j > 0 and i == 0:
        table[i, j] = -np.inf
    elif i > 0:
        table[i, j] = init_gap + (continue_gap * i)
    else:
        table[i, j] = 0


@jit(nopython=True)
def _init_match(table: np.array, init_gap: float, continue_gap: float, i: int, j: int):
    """
    Initializes a cell of the table that tracks the matched pairs of the alignments.

    :param table: The table to initialize.
    :type table: np.array
    :param init_gap: Penalty for initiating a gap sequence in the alignment.
    :type init_gap: float
    :param continue_gap: Penalty for continuing a gap sequence in the alignment.
    :type continue_gap: float
    :param i: The row index of the cell.
    :type i: int
    :param j: The column index of the cell.
    :type j: int
    """
    # if j == 0 and i == 0:
    #   self._table[i, j, 0] = 0
    #   self._table[i, j, 1] = 0 # Deletion
    # else:
    if j == 0 and not i == 0:
        # self._table[i, j, 0] = 0  # Deletion
        table[i, j, 1] = init_gap + continue_gap * i
    elif i == 0 and not j == 0:
        table[i, j, 0] = 1  # Insertion
        table[i, j, 1] = init_gap + continue_gap * j


@jit(nopython=True)
def _initialize_matrices(table: np.array, deletion_table: np.array, insertion_table: np.array,
                         init_gap: float, continue_gap: float):
    """
    Calculates the values of the Dynamic Programming Matrix and stores them in self._table.

    Coding for the matrix
    deletion : 0
    insertion : 1
    mismatch : 2
    match : 3
    """
    for i in range(0, table.shape[0]):
        for j in range(0, table.shape[1]):
            _init_match(table, init_gap, continue_gap, i, j)
            _init_deletion(deletion_table, init_gap, continue_gap, i, j)
            _init_insertion(insertion_table, init_gap, continue_gap, i, j)
