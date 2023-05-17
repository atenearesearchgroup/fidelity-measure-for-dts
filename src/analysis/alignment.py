from typing import List, Tuple

import numpy as np
import pandas as pd
import similaritymeasures
from scipy.spatial.distance import cityblock, euclidean

from systems_config.system import SystemBase


class Alignment:
    PREFIX_DT = 'dt-'
    PREFIX_PT = 'pt-'
    MATCH_OPERATION = 'Match'
    MISMATCH_OPERATION = 'Mismatch'

    def __init__(self, alignment: pd.Dataframe,
                 dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 system: SystemBase,
                 selected_params: List[str]):
        # Traces to align
        self._dt_trace = dt_trace
        self._pt_trace = pt_trace
        # System information
        self._system = system
        # Alignment
        self._alignment = alignment
        # Relevant columns
        self._selected_params = selected_params

    @property
    def percentage_matched_snapshots(self) -> float:
        return self._calculate_percentage(self.MATCH_OPERATION)

    @property
    def percentage_mismatched_snapshots(self) -> float:
        return self._calculate_percentage(self.MISMATCH_OPERATION)

    @property
    def percentage_gaps(self) -> float:
        return 100 - self.percentage_matched_snapshots - self.percentage_mismatched_snapshots

    @property
    def frechet_distances(self) -> tuple[float, float]:
        condition = self._alignment['operation'] == self.MATCH_OPERATION
        matched_dt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_DT).to_numpy()
        matched_pt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_PT).to_numpy()

        frechet_euclidean = similaritymeasures.frechet_dist(matched_dt_snapshots, matched_pt_snapshots, 2)
        frechet_manhattan = similaritymeasures.frechet_dist(matched_dt_snapshots, matched_pt_snapshots, 1)

        return frechet_euclidean, frechet_manhattan

    @property
    def p2p_mean_distances(self) -> tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        condition = self._alignment['operation'] == self.MATCH_OPERATION
        matched_dt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_DT).to_numpy()
        matched_pt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_PT).to_numpy()

        p2p_euclidean = self._calculate_p2p_distance(matched_dt_snapshots, matched_pt_snapshots, 'euclidean')
        p2p_manhattan = self._calculate_p2p_distance(matched_dt_snapshots, matched_pt_snapshots, 'cityblock')

        return p2p_euclidean, p2p_manhattan

    @property
    def number_of_gaps(self) -> int:
        return int(np.sum(self._count_gaps()))

    @property
    def number_of_groups_of_gaps(self) -> int:
        return len(self._count_gaps())

    @property
    def mean_length_gaps(self) -> Tuple[float, float]:
        return float(np.mean(self._count_gaps())), float(np.std(self._count_gaps()))

    def _calculate_p2p_distance(self, dt_matched_snapshots: np.ndarray, pt_matched_snapshots: np.ndarray,
                                metric: str = 'euclidean') -> Tuple[float, float, float]:
        distance_func = {
            'euclidean': euclidean,
            'cityblock': cityblock
        }
        if metric not in distance_func:
            raise ValueError('Invalid distance metric')

        result = [distance_func[metric](dt_matched_snapshots[i], pt_matched_snapshots[i]) for i in
                  range(len(dt_matched_snapshots))]

        return float(np.mean(result, axis=0)), float(np.std(result, axis=0)), float(np.max(result, axis=0))

    def _calculate_percentage(self, operation: str) -> float:
        condition = self._alignment['operation'] == operation
        matched_snapshots = self._get_matched_snapshots(condition, self.PREFIX_DT
        total_snapshots = max(
            self._pt_trace[self._pt_trace != ' '].shape[0],
            self._dt_trace[self._dt_trace != ' '].shape[0]
        )
        return matched_snapshots.shape[0] / total_snapshots * 100

    def _get_matched_snapshots(self, match_condition: pd.Series, prefix: str) -> pd.DataFrame:
        params = [prefix + p for p in self._selected_params]
        matched_trace = self._alignment.loc[match_condition, params].astype(float)
        matched_trace.columns = matched_trace.columns.str.replace(prefix, '')
        return matched_trace

    def _calculate_gaps(self) -> Tuple[int, int, float, float]:
        gap_lengths = self._count_gaps()

        if gap_lengths:
            gap_number = len(gap_lengths)
            gap_total_numer = np.sum(gap_lengths)
            gap_mean_length = np.mean(gap_lengths)
            gap_std_length = np.std(gap_lengths)
        else:
            gap_number = 0
            gap_total_numer = 0
            gap_mean_length = 0.0
            gap_std_length = 0.0

        return gap_number, gap_total_numer, gap_mean_length, gap_std_length

    def _count_gaps(self) -> List[int]:
        gap_cont = 0
        gap_lengths = []
        for i in range(len(self._alignment['operation'])):
            if self._alignment['operation'][i] == 'Insertion' or self._alignment['operation'][i] == 'Deletion':
                gap_cont += 1  # Increase gap counter
            else:
                if gap_cont > 0:  # Gap ended
                    gap_lengths.append(gap_cont)  # Add gap length
                    gap_cont = 0  # Reset counter
        return gap_lengths
