from __future__ import annotations

from typing import List

import pandas as pd

from metrics.ndw.ndw_alignment import NeedlemanWunschAlignmentMetrics
from packages.discrete_frechet.discrete import FastDiscreteFrechetMatrix, manhattan, euclidean
from systems.system import SystemBase


class NeedlemanWunschAlignmentMetricsLCA(NeedlemanWunschAlignmentMetrics):
    def __init__(self, alignment: pd.DataFrame,
                 dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 system: SystemBase,
                 selected_params: List[str],
                 score: float,
                 timestamp_label: str):
        super().__init__(alignment, dt_trace, pt_trace, system, selected_params, score,
                         timestamp_label)
        self._pt_matched_relevant = self._get_relevant_snapshots(
            self._matched_dt_snapshots,
            self._matched_pt_snapshots)
        self._dt_matched_relevant = self._get_relevant_snapshots(
            self._matched_dt_snapshots,
            self._matched_pt_snapshots)

        self._pt_trace_relevant = self._get_relevant_snapshots(self._pt_trace)
        self._dt_trace_relevant = self._get_relevant_snapshots(self._dt_trace)

    @property
    def percentage_matched_snapshots_lca(self) -> float:
        if self._pt_trace_relevant.shape[0] > 0:
            return (self._pt_matched_relevant.shape[0] + self._dt_matched_relevant.shape[0]) \
                / (self._pt_trace_relevant.shape[0] + self._dt_trace_relevant.shape[0]) * 100
        return 0

    @property
    def percentage_mismatched_snapshots_lca(self) -> float:
        condition = self._alignment['operation'] == self.MISMATCH_OPERATION
        mismatched_pt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_PT)
        mismatched_dt_snapshots = self._get_matched_snapshots(condition, self.PREFIX_DT)
        mismatched_relevant_snapshots = self._get_relevant_snapshots(mismatched_pt_snapshots,
                                                                     mismatched_dt_snapshots)
        mismatched_relevant_snapshots += self._get_relevant_snapshots(mismatched_dt_snapshots,
                                                                      mismatched_pt_snapshots)
        if (self._pt_trace_relevant.shape[0] + self._dt_trace_relevant.shape[0]) > 0:
            return ((mismatched_relevant_snapshots.shape[0] / (self._pt_trace_relevant.shape[0] +
                                                               self._dt_trace_relevant.shape[
                                                                   0])) * 100)
        return 0

    @property
    def percentage_gaps_lca(self) -> float:
        return 100 - self.percentage_matched_snapshots_lca - \
            self.percentage_mismatched_snapshots_lca

    def _get_relevant_snapshots(self, snaps, condition_snaps=None):
        snap_filter = ~self._system.filter_low_complexity(
            snaps[self._selected_params])
        if condition_snaps is not None:
            snap_filter = snap_filter | ~self._system.filter_low_complexity(
                condition_snaps[self._selected_params])
        relevant_snapshots = snaps.loc[snap_filter, self._selected_params]
        return relevant_snapshots

    @property
    def frechet_lca(self) -> dict:
        if not (
                self._dt_matched_relevant.empty and self._pt_matched_relevant.empty):
            frechet_euclidean = FastDiscreteFrechetMatrix(euclidean).distance(
                self._dt_matched_relevant.to_numpy(),
                self._pt_matched_relevant.to_numpy())
            frechet_manhattan = FastDiscreteFrechetMatrix(manhattan).distance(
                self._dt_matched_relevant.to_numpy(),
                self._pt_matched_relevant.to_numpy())
        else:
            frechet_euclidean = 0
            frechet_manhattan = 0
        return {'euclidean': frechet_euclidean, 'manhattan': frechet_manhattan}

    @property
    def p2p_mean_lca(self) -> dict:
        p2p_euclidean = self._calculate_p2p_distance(self._dt_matched_relevant,
                                                     self._pt_matched_relevant,
                                                     'euclidean')
        p2p_manhattan = self._calculate_p2p_distance(self._dt_matched_relevant,
                                                     self._pt_matched_relevant,
                                                     'cityblock')

        return {'euclidean': p2p_euclidean, 'manhattan': p2p_manhattan}
