from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from algorithm.case_study import CaseStudyBase


class NeedlemanWunschBase(ABC):

    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 case_study: CaseStudyBase,
                 timestamp_label: str = "timestamp(s)",
                 initiate_gap: float = -0.2,
                 continue_gap: float = 0):
        self._dt_trace = dt_trace
        self._pt_trace = pt_trace
        self._case_study = case_study
        self._table = np.zeros((len(dt_trace), len(pt_trace), 2))
        self._timestamp_label = timestamp_label
        self._initiate_gap = initiate_gap


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

    def calculate_alignment(self) -> (list, list):
        self.calculate_matrix()
        return self.build_result()

    @property
    def initiate_gap(self):
        return self._initiate_gap
