"""
algorithm.factory
~~~~~~~~~~~~~~~~

Factory class for creating instances of alignment algorithms.
"""
from algorithm.dtw.lugaresi import DynamicTimeWarpingLugaresi
from algorithm.dtw.snaps import DynamicTimeWarpingSnaps
from algorithm.lcss.events import LongestCommonSubsequenceEvents
from algorithm.lcss.kpis import LongestCommonSubsequenceKPI
from algorithm.ndw.affine_gap import NeedlemanWunschAffineGap
from algorithm.ndw.constant_gap import NeedlemanWunschConstantGap
from .ialgorithm import IAlignmentAlgorithm


class AlignmentAlgorithmFactory:
    """
    Factory class for creating instances of alignment algorithms.

    This class provides a method to create instances of alignment algorithms, such as the
    Needleman-Wunsch algorithm, Dynamic Time Warping and Longest Common Subsequence with different
    variations, based on the specified algorithm name.

    Some of these variations were presented by Lugaresi et al. in [1]

    References:
        [1] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta: Online validation of
        digital twins for manufacturing systems. Comput. Ind. 150: 103942 (2023)
    """

    @staticmethod
    def get_alignment_algorithm(algorithm, **kwargs) -> IAlignmentAlgorithm:
        """
        Create an instance of the specified alignment algorithm with the given keyword
        arguments.

        :param algorithm: The name of the alignment algorithm to create. It should be one of the
            following:
            - 'NDW_Affine': Needleman-Wunsch algorithm with affine gap penalty.
            - 'NDW_Tolerance': Needleman-Wunsch algorithm with tolerance-based scoring.
            - 'DTW_Snaps': Dynamic Time Warping algorithm to align snapshots
            - 'DTW_Lugaresi': Dynamic Time Warping algorithm to align strings that returns a value
            between 0 and 1 to measure similarity [1].
            - 'LCSS_KPIs': Longest Common Subsequence algorithm modified to align numerical values
            and provide a value between 0 and 1 to measure similarity [1].
            - 'LCSS_Events': Longest Common Subsequence algorithm modified to align strings that
            represent sequences of discrete events in a system. It returns a value between 0
            and 1 to measure similarity [1].
        :param kwargs: Additional keyword arguments to pass to the chosen alignment algorithm's
            constructor.
        :return: AlignmentAlgorithm: An instance of the selected alignment algorithm.
        :raise: ValueError: If an invalid input algorithm name is provided.

        References:
            [1] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta: Online validation of
            digital twins for manufacturing systems. Comput. Ind. 150: 103942 (2023)
        """
        algorithms = {
            'NDW_Affine': NeedlemanWunschAffineGap,
            'NDW_Tolerance': NeedlemanWunschConstantGap,
            'DTW_Snaps': DynamicTimeWarpingSnaps,
            'DTW_Lugaresi': DynamicTimeWarpingLugaresi,
            'LCSS_KPIs': LongestCommonSubsequenceKPI,
            'LCSS_Events': LongestCommonSubsequenceEvents
        }
        if algorithm in algorithms:
            return algorithms[algorithm](**kwargs)
        raise ValueError(f'Invalid input algorithm name {algorithm}.')
