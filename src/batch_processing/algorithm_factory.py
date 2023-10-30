from algorithm import NeedlemanWunschAffineGap, NeedlemanWunschTolerance, AlignmentAlgorithm

NDW_AFFINE = "NDW_Affine"
NDW_TOLERANCE = "NDW_Tolerance"


class AlignmentAlgorithmFactory:
    """
    Factory class for creating instances of alignment algorithms.

    This class provides a method to create instances of alignment algorithms, such as the
    Needleman-Wunsch algorithm with different variations, based on the specified algorithm name.

    Methods:
        get_alignment_algorithm(algorithm, **kwargs) -> AlignmentAlgorithm:
            Create an instance of the specified alignment algorithm with the given keyword
            arguments.

    Parameters:
        algorithm (str): The name of the alignment algorithm to create. It should be one of the
        following:
            - NDW_Affine: Needleman-Wunsch algorithm with affine gap penalties.
            - NDW_Tolerance: Needleman-Wunsch algorithm with tolerance-based scoring.
        **kwargs: Additional keyword arguments to pass to the chosen alignment algorithm's
        constructor.

    Returns:
        AlignmentAlgorithm: An instance of the selected alignment algorithm.

    Raises:
        ValueError: If an invalid input algorithm name is provided.
    """

    @staticmethod
    def get_alignment_algorithm(algorithm, **kwargs) -> AlignmentAlgorithm:
        if algorithm == NDW_AFFINE:
            return NeedlemanWunschAffineGap(**kwargs)
        elif algorithm == NDW_TOLERANCE:
            return NeedlemanWunschTolerance(**kwargs)
        else:
            raise ValueError(f'Invalid input algorithm name {algorithm}.')
