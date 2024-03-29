import numpy as np

from batch_processing import AlignmentConfiguration


class LongestCommonSubsequenceEventsConfig(AlignmentConfiguration):
    DELTA = 'delta'
    TIMESTAMP_LABEL = 'timestamp_label'
    PARAM_INTEREST = 'param_interest'

    def __init__(self, current_directory, args, config):
        super().__init__(current_directory, args, config)

        ranges = self._config['ranges']

        # Calculate Maximum Acceptable Distance (MAD)
        self._delta = np.arange(
            ranges['delta']['start'],
            ranges['delta']['end'],
            ranges['delta']['step']
        )

    def _get_hyperparameters_labels(self) -> list:
        return [self.DELTA]

    def _get_hyperparameters_ranges(self) -> list:
        return [self._delta]

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            **super().get_config_params(pt_trace, dt_trace, current_config),
            self.TIMESTAMP_LABEL: self._timestamp_label,
            self.PARAM_INTEREST: self._param_interest,
            **current_config
        }
