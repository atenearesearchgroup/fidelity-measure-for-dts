from typing import List

import numpy as np
import pandas as pd
from scipy.spatial.distance import cityblock, euclidean

from metrics.alignment_base import AlignmentBase
from packages.discrete_frechet.discrete import FastDiscreteFrechetMatrix, manhattan
from systems.system import SystemBase


class NeedlemanWunschAlignmentMetrics(AlignmentBase):
    MATCH_OPERATION = 'Match'
    MISMATCH_OPERATION = 'Mismatch'

    def __init__(self, alignment: pd.DataFrame,
                 dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 system: SystemBase,
                 selected_params: List[str],
                 score: float,
                 timestamp_label: str):
        super().__init__(alignment, dt_trace, pt_trace, system, selected_params, score,
                         timestamp_label)

        condition = self._alignment['operation'] == self.MATCH_OPERATION
        self._matched_dt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_DT)
        self._matched_pt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_PT)
        # Gaps
        self._gaps = self._count_gaps()

    @property
    def percentage_matched_snapshots(self) -> float:
        return self._calculate_percentage(self._matched_dt_snapshots.to_numpy())

    @property
    def percentage_mismatched_snapshots(self) -> float:
        condition = self._alignment['operation'] == self.MISMATCH_OPERATION
        mismatched_snapshots = self._get_matched_snapshots(condition, self.PREFIX_DT).to_numpy()
        return self._calculate_percentage(mismatched_snapshots)

    @property
    def percentage_gaps(self) -> float:
        return 100 - self.percentage_matched_snapshots - self.percentage_mismatched_snapshots

    @property
    def frechet(self) -> dict:
        if not (self._matched_dt_snapshots.empty and self._matched_pt_snapshots.empty):
            frechet_euclidean = FastDiscreteFrechetMatrix(euclidean).distance \
                (self._matched_dt_snapshots.to_numpy(), self._matched_pt_snapshots.to_numpy())
            frechet_manhattan = FastDiscreteFrechetMatrix(manhattan).distance \
                (self._matched_dt_snapshots.to_numpy(), self._matched_pt_snapshots.to_numpy())
        else:
            frechet_euclidean = 0
            frechet_manhattan = 0

        return {'euclidean': frechet_euclidean, 'manhattan': frechet_manhattan}

    @property
    def p2p_mean(self) -> dict:
        p2p_euclidean = self._calculate_p2p_distance(self._matched_dt_snapshots,
                                                     self._matched_pt_snapshots)
        p2p_manhattan = self._calculate_p2p_distance(self._matched_dt_snapshots,
                                                     self._matched_pt_snapshots,
                                                     'cityblock')

        return {'euclidean': p2p_euclidean, 'manhattan': p2p_manhattan}

    @property
    def number_of_gaps(self) -> int:
        return int(np.sum(self._gaps))

    @property
    def number_of_groups_of_gaps(self) -> int:
        return len(self._gaps)

    @property
    def mean_length_gaps(self) -> dict:
        if self._gaps:
            return {'mean': float(np.mean(self._gaps)), 'std': float(np.std(self._gaps))}
        else:
            return {'mean': 0, 'std': 0}

    @staticmethod
    def _calculate_p2p_distance(matched_pt_snapshots: pd.DataFrame,
                                matched_dt_snapshots: pd.DataFrame,
                                metric: str = 'euclidean') -> dict:
        distance_func = {
            'euclidean': euclidean,
            'cityblock': cityblock
        }
        if metric not in distance_func:
            raise ValueError('Invalid distance metric')
        matched_pt_snapshots = matched_pt_snapshots.to_numpy()
        matched_dt_snapshots = matched_dt_snapshots.to_numpy()
        result = [distance_func[metric](matched_dt_snapshots[i], matched_pt_snapshots[i]) for i in
                  range(len(matched_dt_snapshots))]

        if result:
            return {'mean': float(np.mean(result, axis=0)),
                    'std': float(np.std(result, axis=0)),
                    'max': float(np.max(result, axis=0))}
        else:
            return {'mean': 0,
                    'std': 0,
                    'max': 0}

    def _calculate_percentage(self, matched_snapshots: np.ndarray) -> float:
        total_snapshots = max(
            self._pt_trace[self._pt_trace != ' '].shape[0],
            self._dt_trace[self._dt_trace != ' '].shape[0]
        )
        return matched_snapshots.shape[0] / total_snapshots * 100

    def _get_matched_snapshots(self, match_condition: bool, prefix: str) -> pd.DataFrame:
        params = [prefix + p for p in self._selected_params]

        numeric_columns = []
        for p in params:
            if self._alignment[p].apply(lambda x: isinstance(x, (float, int)) and
                                                  not isinstance(x, bool)).any():
                numeric_columns.append(p)

        # Filter the DataFrame to select only numeric columns
        # matched_trace = self._alignment[numeric_columns]
        matched_trace = self._alignment.loc[match_condition, numeric_columns]
        matched_trace.columns = matched_trace.columns.str.replace(prefix, '')
        return matched_trace

    def _count_gaps(self) -> List[int]:
        gap_cont = 0
        gap_lengths = []
        for i in range(len(self._alignment['operation'])):
            if self._alignment['operation'][i] == 'Insertion' \
                    or self._alignment['operation'][i] == 'Deletion':
                gap_cont += 1  # Increase gap counter
            else:
                if gap_cont > 0:  # Gap ended
                    gap_lengths.append(gap_cont)  # Add gap length
                    gap_cont = 0  # Reset counter
        return gap_lengths
