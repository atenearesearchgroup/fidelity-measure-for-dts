from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from algorithm.alignment_algorithm import AlignmentAlgorithm
from systems.system import SystemBase


class NeedlemanWunschBase(ABC, AlignmentAlgorithm):
    """
    Abstract Class for performing sequence alignment using the Needleman-Wunsch algorithm
    which does not include any gap penalty strategy.

    The Needleman-Wunsch algorithm is a dynamic programming algorithm used to globally align
    two sequences. This version includes the alignment of not only characters but any type
    of snapshot, which is a list of attributes.

    References:
        - Needleman, S.B., and Wunsch, C.D. (1970). A general method applicable to the search for
          similarities in the amino acid sequence of two proteins. Journal of Molecular Biology,
          48(3), 443-453.
    """
    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 system: SystemBase,
                 timestamp_label: str = "timestamp(s)",
                 init_gap: float = -0.2,
                 cont_gap: float = 0,
                 mad: dict = None):
        # Traces to align
        self._continue_gap = cont_gap
        self._dt_trace = dt_trace
        self._pt_trace = pt_trace
        # System information
        self._system = system
        # Configuration
        self._timestamp_label = timestamp_label
        self._init_gap = init_gap
        self._mad = mad
        # Alignment table to calculate alignment
        self._table = np.zeros((len(dt_trace), len(pt_trace), 2))

    def build_result(self) -> pd.DataFrame:
        dt_size = len(self._table) - 1
        pt_size = len(self._table[0, :, :]) - 1
        keys = self._pt_trace[0].keys()
        rows = []

        # Add headers to file
        headers = ["dt-" + k for k in keys]
        headers.extend(["pt-" + k for k in keys])
        headers.append("operation")

        while dt_size > 0 or pt_size > 0:
            row = []
            if pt_size > 0:
                if self._table[dt_size, pt_size, 0] == 1:  # Insertion
                    aux = []
                    for key in keys:
                        row.append("-")
                        aux.append(self._pt_trace[pt_size][key])  # - 1

                    row.extend(aux)
                    row.append("Insertion")
                    pt_size -= 1
                    rows.insert(0, row)
                    continue

            if dt_size > 0 and pt_size > 0:
                if self._table[dt_size, pt_size, 0] > 1:  # Match or mismatch
                    aux = []
                    for key in keys:
                        row.append(self._dt_trace[dt_size][key])  # - 1
                        aux.append(self._pt_trace[pt_size][key])  # - 1
                    row.extend(aux)
                    if self._table[dt_size, pt_size, 0] > 2:
                        row.append("Match")
                    else:
                        row.append("Mismatch")
                    dt_size -= 1
                    pt_size -= 1
                    rows.insert(0, row)
                    continue

            aux = []  # Must be a deletion
            for key in keys:
                row.append(self._dt_trace[dt_size][key])  # - 1
                aux.append("-")
            row.extend(aux)
            row.append("Deletion")
            dt_size -= 1
            rows.insert(0, row)

        return pd.DataFrame(rows, columns=headers)

    @abstractmethod
    def calculate_matrix(self) -> np.ndarray:
        pass

    def calculate_alignment(self) -> pd.DataFrame:
        self.calculate_matrix()
        return self.build_result()

    @property
    def initiate_gap(self):
        return self._init_gap
