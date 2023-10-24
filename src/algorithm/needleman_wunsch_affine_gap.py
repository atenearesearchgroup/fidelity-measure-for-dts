from abc import ABC

import numpy as np

import util.float_util as fu
from algorithm.needleman_wunsch_base import NeedlemanWunschBase
from systems.system import SystemBase


class NeedlemanWunschAffineGap(NeedlemanWunschBase, ABC):

    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 system: SystemBase,
                 timestamp_label: str = "timestamp(s)",
                 initiate_gap: float = -0.2,
                 continue_gap: float = 0,
                 mad: dict = None,
                 low: int = 5):
        super().__init__(dt_trace, pt_trace, system, timestamp_label, initiate_gap=initiate_gap, mad=mad)
        self._continue_gap = continue_gap
        self._low = low

        # -infinite
        self._MIN = -float("inf")

        # Dynamic programming tables
        self._insert_table = np.zeros((len(dt_trace), len(pt_trace), 1))
        self._deletion_table = np.zeros((len(dt_trace), len(pt_trace), 1))

    def _init_deletion(self, i, j):
        if i > 0 and j == 0:
            return self._MIN
        else:
            if j > 0:
                return self._initiate_gap + (self._continue_gap * j)
            else:
                return 0

    def _init_insertion(self, i, j):
        if j > 0 and i == 0:
            return self._MIN
        else:
            if i > 0:
                return self._initiate_gap + (self._continue_gap * i)
            else:
                return 0

    def _init_match(self, i, j):
        # if j == 0 and i == 0:
            # self._table[i, j, 0] = 0
            # self._table[i, j, 1] = 0 # Deletion
        # else:
        if j == 0 and not(i == 0):
            # self._table[i, j, 0] = 0  # Deletion
            self._table[i, j, 1] = self._initiate_gap + (self._continue_gap * i)
        elif i == 0 and not(j == 0):
            self._table[i, j, 0] = 1  # Insertion
            self._table[i, j, 1] = self._initiate_gap + (self._continue_gap * j)

    def calculate_matrix(self) -> np.ndarray:
        """
        Coding for the matrix
        deletion : 0
        insertion : 1
        mismatch : 2
        match : 3
        """
        if self._mad is None:
            self._mad = self._dt_trace[0]

        dt_index = len(self._dt_trace)  # - 1
        pt_index = len(self._pt_trace)  # - 1

        [[self._init_deletion(i, j) for j in range(0, pt_index)] for i in range(0, dt_index)]
        self._deletion_table = np.array(
            [[self._init_deletion(i, j) for j in range(0, pt_index)] for i in range(0, dt_index)])
        self._insert_table = np.array([[self._init_insertion(i, j) for j in range(0, pt_index)] for i in range(0, dt_index)])
        [[self._init_match(i, j) for j in range(0, pt_index)] for i in range(0, dt_index)]

        for j in range(1, pt_index):
            for i in range(1, dt_index):
                self._deletion_table[i][j] = \
                    max((self._initiate_gap + self._continue_gap + self._table[i - 1][j][1]),
                        (self._continue_gap + self._deletion_table[i - 1][j]), )
                self._insert_table[i][j] = \
                    max((self._initiate_gap + self._continue_gap + self._table[i][j - 1][1]),
                        (self._continue_gap + self._insert_table[i][j - 1]))

                equals_value = self._system.snap_equals(self._dt_trace[i],
                                                        self._pt_trace[j],
                                                        self._mad, self._timestamp_label,
                                                        self._low)

                sub = self._table[i - 1, j - 1, 1] + equals_value

                max_value, max_index = fu.max_tolerance(sub,
                                                        self._insert_table[i][j],
                                                        self._deletion_table[i][j],
                                                        equals_value)

                self._table[i, j, 1] = max_value
                self._table[i, j, 0] = max_index  # Match : 3 / Mismatch : 2 / Insertion : 1 / Deletion : 0

        return self._table