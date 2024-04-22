"""
ndw.base
~~~~~~~~~~~~~~~~

Abstract class for the implementation of the Needleman Wunsch algorithm variants.
"""
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from algorithm.logic.ialgorithm import IAlignmentAlgorithm
from systems.system import SystemBase
from util.float import is_numerical


class NeedlemanWunschBase(ABC, IAlignmentAlgorithm):
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

    def __init__(self, dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 system: SystemBase,
                 lca: bool,
                 timestamp_label: str = "timestamp(s)",
                 init_gap: float = -0.2,
                 cont_gap: float = 0,
                 mad: dict = None,
                 low: float = None,
                 include_timestamp: bool = False):
        # Traces to align
        self._dt_trace = dt_trace.to_numpy()
        self._pt_trace = pt_trace.to_numpy()

        # Configuration
        self._init_gap = init_gap
        self._continue_gap = cont_gap
        self._low = low

        # System information
        self._system = system

        # Alignment table to calculate alignment
        self._table = np.zeros((len(dt_trace) + 1, len(pt_trace) + 1, 2))

        # -- Caching values to improve performance of snap_equals --
        # Names of the snapshots' attributes
        self._keys = pt_trace.columns.values.astype(str).tolist()
        # Boolean list containing whether each attribute is numerical or not
        self._types = is_numerical(self._pt_trace[0])
        # Numerical range including the indices of the attributes considered in snap_equals
        self._timestamp_range = self._initialize_timestamp_range(include_timestamp, timestamp_label)
        # mad dictionary into numpy array for numba
        self._mad = self._initialize_mad(include_timestamp, mad, timestamp_label)
        # Low-complexity area tagging for all snapshots
        self._lca = lca
        self._dt_low = self._initialize_low(self._dt_trace)
        self._pt_low = self._initialize_low(self._pt_trace)

    def build_result(self) -> pd.DataFrame:
        """
        Performs backtracking on the Dynamic Programming Matrix to obtain the pairs aligned by
        the algorithm.
        """
        dt_size = len(self._table) - 1
        pt_size = len(self._table[0, :, :]) - 1
        len_snapshot = self._pt_trace.shape[1]
        rows = []

        # Add headers to file
        headers = ["dt-" + k for k in self._keys]
        headers.extend(["pt-" + k for k in self._keys])
        headers.append("operation")

        while dt_size > 0 or pt_size > 0:
            row = []
            if pt_size > 0:
                if self._table[dt_size, pt_size, 0] == 1:  # Insertion
                    aux = []
                    for i in range(len_snapshot):
                        row.append("-")
                        aux.append(self._pt_trace[pt_size - 1, i])  # - 1

                    row.extend(aux)
                    row.append("Insertion")
                    pt_size -= 1
                    rows.insert(0, row)
                    continue

            if dt_size > 0 and pt_size > 0:
                if self._table[dt_size, pt_size, 0] > 1:  # Match or mismatch
                    aux = []
                    for i in range(len_snapshot):
                        row.append(self._dt_trace[dt_size - 1, i])
                        aux.append(self._pt_trace[pt_size - 1, i])
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
            for i in range(len_snapshot):
                row.append(self._dt_trace[dt_size - 1, i])  # - 1
                aux.append("-")
            row.extend(aux)
            row.append("Deletion")
            dt_size -= 1
            rows.insert(0, row)

        return pd.DataFrame(rows, columns=headers)

    @abstractmethod
    def calculate_matrix(self) -> np.ndarray:
        """
        Calculates the values of the Dynamic Programming Matrix and stores them in self._table.
        """

    def calculate_alignment(self) -> pd.DataFrame:
        """
        Calculates the alignment between two sequences or datasets and returns the alignment result.
        This method internally calculates the alignment matrix and constructs the alignment result
        based on it.

        :return: A DataFrame that includes the alignment.
        :rtype: pd.DataFrame
        """
        self.calculate_matrix()
        return self.build_result()

    @property
    def initiate_gap(self):
        """
        Get the penalty for initiating a gap sequence in the alignment.

        :return: Penalty value for initiating a gap sequence in the alignment.
        :rtype: float
        """
        return self._init_gap

    @property
    def score(self):
        """
        The score represents the accumulated score after aligning the pairs and excluding
        the gap penalty.

        :return: The resulting score of the alignment algorithm.
        :rtype: float
        """
        return self._table[-1, -1]

    def _initialize_low(self, trace):
        """
        Initializes the low-complexity matrix based on the given trace. This method intends to
        cache the values of the LCA to prevent repeated calls from snap_equals and improve its
        performance.

        :param trace: Input trace data in the shape (n_snapshots, n_attributes).
        :type trace pd.Dataframe

        :return: Matrix representing the low complexity values. It has the shape (n_snapshots, n_attributes)
                 where each element is a boolean value indicating whether the corresponding feature in
                 the trace belongs to a low-complexity area.
        :rtype: numpy.ndarray
        """
        low = np.zeros((trace.shape[0], len(self._keys)), dtype=bool)
        if self._lca:
            for i in range(len(trace)):
                for j, k in enumerate(self._keys):
                    low[i, j] = self._system.is_low_complexity(k, trace[i, j])

        return low

    def _initialize_timestamp_range(self, include_timestamp, timestamp_label):
        """
        Initializes the parameter timestamp_range that includes the index of the snapshots
        that will be considered in the alignment. This intends to speed up the calls to the
        snap_equals function, preventing from generating these lists each time it is called.

        :param include_timestamp: Flag indicating whether timestamps are considered in alignments.
        :type include_timestamp: bool
        :param timestamp_label: Label identifying the timestamp feature in the keys.
        :type timestamp_label: str

        :return: Array containing indices corresponding to the timestamp features if
        include_timestamp is True, otherwise indices of features excluding the timestamp
        feature specified by timestamp_label.
        :rtype: numpy.ndarray
        """
        if include_timestamp:
            return np.array(range(len(self._keys)))
        else:
            return np.array([index for index, key in enumerate(self._keys) if
                             key != timestamp_label])

    def _initialize_mad(self, include_timestamp, mad, timestamp_label):
        """
        Initializes the Maximum Acceptable Distance (MAD) array based on the provided parameters.

        :param include_timestamp: Flag indicating whether timestamps are included in the keys.
        :type include_timestamp: bool
        :param mad: Dictionary containing the MAD values for each feature.
        :type mad: dict
        :param timestamp_label: Label identifying the timestamp feature in the keys.
        :type timestamp_label: str

        :return: Array containing the MAD values for each feature. If include_timestamp is True,
            MAD values are retrieved directly from the mad dictionary based on the keys. If
            include_timestamp is False, MAD values are retrieved from the mad dictionary for all
            features except the one specified by timestamp_label, which is set to 0.
        :rtype: Numpy.ndarray
        """
        if include_timestamp:
            return np.array([mad[key] for key in self._keys])
        else:
            return np.array([mad[key] if key != timestamp_label else 0
                             for key in self._keys])
