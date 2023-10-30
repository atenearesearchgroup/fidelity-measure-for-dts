from metrics.alignment_lca import AlignmentLCA, Alignment


class AnalysisFactory:
    """
    A factory class for creating instances of `Alignment` and `AlignmentLCA` classes
    based on a given flag (`lca`).
    """

    @staticmethod
    def create_instance(lca, **kwargs):
        return AnalysisFactory.get_class(lca)(**kwargs)

    @staticmethod
    def get_class(lca):
        if lca:
            return AlignmentLCA
        return Alignment
