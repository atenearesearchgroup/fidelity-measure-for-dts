from metrics.dtw.dtw_alignment import DynamicTimeWarpingAlignmentMetrics
from metrics.ndw.ndw_alignment_lca import NeedlemanWunschAlignmentMetricsLCA, \
    NeedlemanWunschAlignmentMetrics


class AnalysisFactory:
    """
    A factory class for creating instances of `Alignment` and `AlignmentLCA` classes
    based on a given flag (`lca`).
    """

    @staticmethod
    def create_instance(algorithm, lca, **kwargs):
        return AnalysisFactory.get_class(algorithm, lca)(**kwargs)

    @staticmethod
    def get_class(algorithm, lca):
        algorithms = {
            'NDW': NeedlemanWunschAlignmentMetrics,
            'NDW_LCA': NeedlemanWunschAlignmentMetricsLCA,
            'DTW': DynamicTimeWarpingAlignmentMetrics,
        }
        algorithm = algorithm[:3]
        if lca:
            algorithm += '_LCA'

        if algorithm in algorithms:
            return algorithms[algorithm]
        raise ValueError(f"Invalid input algorithm name {algorithm}.")
