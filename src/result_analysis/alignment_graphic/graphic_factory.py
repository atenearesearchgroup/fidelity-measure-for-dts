from result_analysis.alignment_graphic.dtw_alignment_graphic import \
    DynamicTimeWarpingAlignmentGraphics
from result_analysis.alignment_graphic.ndw_alignment_graphic import NeedlemanWunschAlignmentGraphics


class GraphicFactory:
    """
    A factory class for generating plots that include the alignments of Needleman-Wunsch and
    Dynamic Time Warping Algorithms
    """

    @staticmethod
    def get_graphic(algorithm, alignment, dt_trace, pt_trace, **kwargs):
        algorithms = {'NDW': NeedlemanWunschAlignmentGraphics,
                      'DTW': DynamicTimeWarpingAlignmentGraphics, }
        algorithm = algorithm[:3]
        if algorithm in algorithms:
            return algorithms[algorithm](alignment, dt_trace, pt_trace,
                                         **kwargs).generate_alignment_graphic()
        return None
