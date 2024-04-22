"""
batch.config.ndw
~~~~~~~~~~~~~~~~

A class that generates alignment batches from a YAML file for the Needleman Wunsch (NDW)
algorithm [1]. It takes the batch configuration from a YAML file, including input ranges and
configuration parameters.

References:
    [1] Needleman, S.B., and Wunsch, C.D. (1970). A general method applicable to the search for
      similarities in the amino acid sequence of two proteins. Journal of Molecular Biology,
      48(3), 443-453.
"""

from algorithm.config.alg_config import AlgorithmConfiguration
from util.dict_util import get_range


class NeedlemanWunschConfiguration(AlgorithmConfiguration):
    """
    A class that generates alignment batches from a YAML file for the Needleman Wunsch (NDW)
    algorithm [1]. It takes the batch configuration from a YAML file, including input ranges and
    configuration parameters.

    References:
        [1] Needleman, S.B., and Wunsch, C.D. (1970). A general method applicable to the search for
          similarities in the amino acid sequence of two proteins. Journal of Molecular Biology,
          48(3), 443-453.
    """
    MAD = 'mad'
    LOW = 'low'
    INIT_GAP = 'init_gap'
    CONT_GAP = 'cont_gap'
    LCA = 'lca'

    def __init__(self, args, config):
        super().__init__(args, config)

        # INPUT PARAMETERS
        ranges = self.config['ranges']

        # Calculate Maximum Acceptable Distance (MAD)
        self._mad = {}
        mad = ranges['mad']
        for p in self.params:
            if p in mad:
                self._mad[p] = get_range(mad[p])

        # Calculate Weight for Low complexity areas
        self._low = get_range(ranges[self.LOW])

        # Calculate Weights for Affine Gap
        self._init_gap = get_range(ranges[self.INIT_GAP])
        self._cont_gap = get_range(ranges[self.CONT_GAP])

    def get_hyperparameters_labels(self) -> list:
        """
        :return: A list of the hyperparameter labels (init_gap, cont_gap, low, mad) for the
        corresponding algorithm.
        """
        return [self.INIT_GAP, self.CONT_GAP, self.LOW,
                *[f"{self.MAD}-{p}" for p in self._mad]]

    def get_hyperparameters_ranges(self) -> list:
        """
        :return: A list of the hyperparameter ranges (init_gap, cont_gap, low, mad) for the
        corresponding algorithm.
        """
        return [self._init_gap, self._cont_gap, self._low, *self._mad.values()]

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        """
        It generates a dictionary containing the necessary input parameters to instantiate the
        given algorithm. The dictionary serves as the creation attributes for the algorithm
        instance.

        :param pt_trace: The Physical Twin Trace
        :param dt_trace: The Digital Twin Trace
        :param current_config: The dictionary with the current configuration for the algorithm
        :return: A dictionary with the configuration parameters and their values.
        """
        return {
            **super().get_config_params(pt_trace, dt_trace, current_config),
            AlgorithmConfiguration.SYSTEM: self.system,
            AlgorithmConfiguration.TIMESTAMP_LABEL: self.timestamp_label,
            self.LCA: self.lca,
        }
