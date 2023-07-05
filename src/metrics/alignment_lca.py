from __future__ import annotations

from typing import List

import pandas as pd
from analysis.alignment import Alignment
from systems_config.system import SystemBase

from packages.discrete_frechet.discrete import FastDiscreteFrechetMatrix, manhattan, euclidean


class AlignmentLCA(Alignment):
    def __init__(self, alignment: pd.Dataframe,
                 dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 system: SystemBase,
                 selected_params: List[str]):
        super().__init__(alignment, dt_trace, pt_trace, system, selected_params)
        self._pt_matched_relevant_snapshots = self._get_relevant_snapshots(self._matched_dt_snapshots,
                                                                           self._matched_pt_snapshots)
        self._dt_matched_relevant_snapshots = self._get_relevant_snapshots(self._matched_pt_snapshots)

    @property
    def percentage_matched_snapshots_lca(self) -> float:
        pt_relevant_snapshots = self._get_relevant_snapshots(self._pt_trace)
        return (self._pt_matched_relevant_snapshots.shape[0] / pt_relevant_snapshots.shape[0]) * 100

    @property
    def percentage_mismatched_snapshots_lca(self) -> float:
        condition = self._alignment['operation'] == self.MISMATCH_OPERATION
        mismatched_pt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_PT)
        pt_mismatched_relevant_snapshots = self._get_relevant_snapshots(mismatched_pt_snapshots)
        pt_relevant_snapshots = self._get_relevant_snapshots(self._pt_trace)
        return (pt_mismatched_relevant_snapshots.shape[0] / pt_relevant_snapshots.shape[0]) * 100

    @property
    def percentage_gaps_lca(self) -> float:
        return 100 - self.percentage_matched_snapshots_lca - self.percentage_mismatched_snapshots_lca

    def _get_relevant_snapshots(self, snapshots, condition_snapshots=None):
        if condition_snapshots is None:
            condition_snapshots = snapshots
        relevant_snapshots = snapshots.loc[
            ~self._system.is_low_complexity(condition_snapshots[self._selected_params]), self._selected_params]
        return relevant_snapshots

    @property
    def frechet_lca(self) -> dict:
        if not (self._dt_matched_relevant_snapshots.empty and self._pt_matched_relevant_snapshots.empty):
            frechet_euclidean = FastDiscreteFrechetMatrix(euclidean).distance(
                self._dt_matched_relevant_snapshots.to_numpy(),
                self._pt_matched_relevant_snapshots.to_numpy())
            frechet_manhattan = FastDiscreteFrechetMatrix(manhattan).distance(
                self._dt_matched_relevant_snapshots.to_numpy(),
                self._pt_matched_relevant_snapshots.to_numpy())
        else:
            frechet_euclidean = 0
            frechet_manhattan = 0
        return {'euclidean': frechet_euclidean, 'manhattan': frechet_manhattan}

    @property
    def p2p_mean_lca(self) -> dict:
        p2p_euclidean = self._calculate_p2p_distance(self._dt_matched_relevant_snapshots,
                                                     self._pt_matched_relevant_snapshots, 'euclidean')
        p2p_manhattan = self._calculate_p2p_distance(self._dt_matched_relevant_snapshots,
                                                     self._pt_matched_relevant_snapshots, 'cityblock')

        return {'euclidean': p2p_euclidean, 'manhattan': p2p_manhattan}
