from abc import ABC

import numpy as np
import pandas as pd

import util.float_util as fu

from algorithm.needleman_wunsch_base import NeedlemanWunschBase


class NeedlemanWunschTolerance(NeedlemanWunschBase, ABC):

    def calculate_matrix(self) -> np.ndarray:
        """
        Coding for the matrix
        deletion : 0
        insertion : 1
        mismatch : 2
        match : 3
        """
        if self._tolerance is None:
            self._tolerance = self._dt_trace[0]

        dt_index = len(self._dt_trace)  # - 1
        pt_index = len(self._pt_trace)  # - 1

        # table[0, 0, 0] = 0  # Initialization first cell
        # table[0, 0, 1] = 0

        for j in range(1, pt_index):  # + 1
            self._table[0, j, 0] = 1  # Insertion
            self._table[0, j, 1] = self._table[0, j - 1, 1] + self._initiate_gap

        for i in range(1, dt_index):  # + 1
            # table[i, 0, 0] = 0  # Deletion
            self._table[i, 0, 1] = self._table[i - 1, 0, 1] + self._initiate_gap

            for j in range(1, pt_index):
                equals_value = self._case_study.snap_equals(self._dt_trace[i],  # [i - 1]
                                                self._pt_trace[j],  # [j - 1]
                                                self._tolerance,
                                                self._timestamp_label)

                sub = self._table[i - 1, j - 1, 1] + equals_value  # Match/Mismatch
                ins = self._table[i, j - 1, 1] + self._initiate_gap  # Insertion
                dele = self._table[i - 1, j, 1] + self._initiate_gap  # Deletion

                max_value, max_index = fu.max_tolerance(sub, ins, dele, equals_value)

                self._table[i, j, 1] = max_value
                self._table[i, j, 0] = max_index  # Match : 3 / Mismatch : 2 / Insertion : 1 / Deletion : 0

        return self._table








