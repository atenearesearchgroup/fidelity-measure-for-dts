import numpy as np

from batch_processing import AlignmentConfiguration


class LongestCommonSubsequenceKPIsConfig(AlignmentConfiguration):
    EPSILON = 'epsilon'
    PARAM_INTEREST = 'param_interest'

    def __init__(self, current_directory, config):
        super().__init__(current_directory, config)

        ranges = self._config['ranges']

        # Calculate Maximum Acceptable Distance (MAD)
        self._epsilon = np.arange(
            ranges['epsilon']['start'],
            ranges['epsilon']['end'],
            ranges['epsilon']['step']
        )

    def _get_hyperparameters_labels(self) -> list:
        return [self.EPSILON]

    def _get_hyperparameters_ranges(self) -> list:
        return [self._epsilon]

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            **super().get_config_params(pt_trace, dt_trace, current_config),
            self.PARAM_INTEREST: self._param_interest,
            **current_config
        }
