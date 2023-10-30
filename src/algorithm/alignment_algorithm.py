import abc

import pandas as pd


class AlignmentAlgorithm(metaclass=abc.ABCMeta):
    """
    Abstract base class for alignment algorithms.

    This class defines the interface for alignment algorithms that can calculate alignments
    between two sequences. Subclasses must implement the `calculate_alignment`
    method.

    Methods:
        calculate_alignment(self) -> (list, list): Calculate the alignment between two sequences
        or data sets and return the alignment result as a DataFrame.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'calculate_alignment') and
                callable(subclass.calculate_alignment) or
                NotImplemented)

    @abc.abstractmethod
    def calculate_alignment(self) -> pd.DataFrame:
        """
        Calculate the alignment between two sequences or data sets and return the alignment result
        :return: a DataFrame that includes the alignment
        """
        raise NotImplementedError
