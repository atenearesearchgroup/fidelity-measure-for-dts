"""
lcss.kpis
~~~~~~~~~~~~~~~~

Implementation of Longest Common Subsequence (LCS) [1] algorithm for aligning sequences of KPIs,
as proposed in [2].

References:
    [1] David Maier (1978). "The Complexity of Some Problems on Subsequences and
    Supersequences". J. ACM. ACM Press. 25 (2): 322–336
    [2] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
    Online validation of digital twins for manufacturing systems. Comput.
    Ind. 150: 103942 (2023)
"""

from algorithm.lcss.base import LongestCommonSubsequenceBase


class LongestCommonSubsequenceKPI(LongestCommonSubsequenceBase):
    """
    LongestCommonSubsequenceKPI implements a variation of the Longest Common Subsequence (LCS)[1]
    algorithm for aligning sequences of KPI values, as proposed in [2].

    The longest common subsequence (LCS) is the longest subsequence common to all sequences in a set
    of sequences (often just two sequences).

    References:
        [1] David Maier (1978). "The Complexity of Some Problems on Subsequences and
        Supersequences". J. ACM. ACM Press. 25 (2): 322–336
        [2] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
        Online validation of digital twins for manufacturing systems. Comput.
        Ind. 150: 103942 (2023)
    """

    def __init__(self, dt_trace: list,
                 pt_trace: list,
                 param_interest: str,
                 epsilon: float):
        super().__init__(dt_trace, pt_trace, param_interest)
        self._epsilon = epsilon

    def equals_condition(self, dt_snap, pt_snap) -> bool:
        """
        Returns whether the snapshots dt_snap and pt_snap are equal or not: the difference between
        their values must be below a threshold named epsilon.
        """
        return abs(dt_snap[self._param_interest] - pt_snap[self._param_interest]) \
            <= self._epsilon
