from algorithm.lcss.longest_common_subsequence_base import LongestCommonSubsequenceBase


class LongestCommonSubsequenceKPI(LongestCommonSubsequenceBase):

    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 param_interest: str,
                 epsilon: float):
        super().__init__(dt_trace, pt_trace, param_interest)
        self._epsilon = epsilon

    def equals_condition(self, dt_snap, pt_snap) -> bool:
        # if not (isinstance(dt_snap[self._param_of_interest], (float, int))
        #         and isinstance(pt_snap[self._param_of_interest], (float, int))):
        #     raise ValueError('This algorithm only allows comparison between numeric types')
        return abs(dt_snap[self._param_interest] - pt_snap[self._param_interest]) \
            <= self._epsilon
