from algorithm.lcss.longest_common_subsequence_base import LongestCommonSubsequenceBase

"""
Taken from for comparison purposes:
Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
Online validation of digital twins for manufacturing systems. Comput. Ind. 150: 103942 (2023)
"""
class LongestCommonSubsequenceEvents(LongestCommonSubsequenceBase):

    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 param_interest: str,
                 delta: float,
                 timestamp_label: str = 'timestamp(s)'):
        super().__init__(dt_trace, pt_trace, param_interest)
        self._delta = delta
        self._timestamp_label = timestamp_label

    def equals_condition(self, dt_snap, pt_snap) -> bool:
        # if not (isinstance(dt_snap[self._param_of_interest], str)
        #         and isinstance(pt_snap[self._param_of_interest], str)):
        #     raise ValueError('This algorithm only allows comparison between strings')
        return dt_snap[self._param_interest] == pt_snap[self._param_interest] and \
            abs(dt_snap[self._timestamp_label] - pt_snap[self._timestamp_label]) <= self._delta
