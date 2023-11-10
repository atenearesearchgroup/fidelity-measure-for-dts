from metrics.alignment_base import AlignmentBase


class LCSSAlignmentMetrics(AlignmentBase):
    @property
    def score(self) -> float:
        return self._score

    @property
    def normalized_score(self) -> float:
        return self._score / min(len(self._dt_trace), len(self._pt_trace))
