"""
batch.config.lcss_kpis
~~~~~~~~~~~~~~~~

A class that generates alignment batches for the adaptation of Longest Common Subsequence (LCSS) [1]
algorithm for aligning sequences of KPI values, as proposed in [2]. It takes the batch configuration
from a YAML file, including input ranges and configuration parameters.

References:
    [1] David Maier (1978). "The Complexity of Some Problems on Subsequences and
    Supersequences". J. ACM. ACM Press. 25 (2): 322–336
    [2] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
    Online validation of digital twins for manufacturing systems. Comput.
    Ind. 150: 103942 (2023)
"""
import numpy as np

from batch.config.alg_config import AlgorithmConfiguration


class LongestCommonSubsequenceKPIsConfig(AlgorithmConfiguration):
    """
    A class that generates alignment batches for the adaptation of Longest Common Subsequence (LCSS)
    [1] algorithm for aligning sequences of KPI values, as proposed in [2]. It takes the batch
    configuration from a YAML file, including input ranges and configuration parameters.

    References:
        [1] David Maier (1978). "The Complexity of Some Problems on Subsequences and
        Supersequences". J. ACM. ACM Press. 25 (2): 322–336
        [2] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
        Online validation of digital twins for manufacturing systems. Comput.
        Ind. 150: 103942 (2023)
    """
    EPSILON = 'epsilon'

    def __init__(self, current_directory, args, config):
        super().__init__(current_directory, args, config)

        ranges = self.config['ranges']

        self._epsilon = np.arange(
            ranges['epsilon']['start'],
            ranges['epsilon']['end'],
            ranges['epsilon']['step']
        )

    def get_hyperparameters_labels(self) -> list:
        """
        :return: A list of the hyperparameter labels (epsilon) for the corresponding algorithm.
        """
        return [self.EPSILON]

    def get_hyperparameters_ranges(self) -> list:
        """
        :return: A list of the hyperparameter ranges (epsilon) for the corresponding algorithm.
        """
        return [self._epsilon]

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
            AlgorithmConfiguration.PARAM_INTEREST: self._param_interest
        }
