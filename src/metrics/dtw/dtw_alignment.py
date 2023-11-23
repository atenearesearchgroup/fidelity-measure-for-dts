from metrics.alignment_base import AlignmentBase


class DynamicTimeWarpingAlignmentMetrics(AlignmentBase):
    @property
    def score(self) -> float:
        return self._score

    @property
    def normalized_score(self) -> float:
        return 1 - self._score / max(len(self._dt_trace), len(self._pt_trace))


class DynamicTimeWarpingSnapsAlignmentMetrics(AlignmentBase):
    def _number_one_to_many(self, prefix, trace):
        column_name = prefix + self._timestamp_label
        return len(self._alignment[column_name]) - len(trace)

    @property
    def number_one_to_many_pt(self):
        return self._number_one_to_many(self.PREFIX_PT, self._pt_trace)

    @property
    def number_one_to_many_dt(self):
        return self._number_one_to_many(self.PREFIX_DT, self._dt_trace)

    def _times_a_snap_is_aligned(self, prefix):
        column_name = prefix + self._timestamp_label
        repeated_values_count = self._alignment[column_name].value_counts()
        return {f'max_rep': repeated_values_count.max(),
                f'number_rep': len(repeated_values_count[repeated_values_count > 1]),
                f'avg_rep': repeated_values_count[repeated_values_count > 1].mean(),
                f'std_rep': repeated_values_count[repeated_values_count > 1].std()}

    @property
    def pt_snap_aligned(self):
        return self._times_a_snap_is_aligned(self.PREFIX_PT)

    @property
    def dt_snap_aligned(self):
        return self._times_a_snap_is_aligned(self.PREFIX_DT)

    @property
    def score(self) -> float:
        return self._score
