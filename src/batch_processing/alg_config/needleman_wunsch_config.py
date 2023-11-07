import numpy as np

from batch_processing.alg_config.alignment_config import AlignmentConfiguration

MAD = 'mad'
LOW = 'low'
INIT_GAP = 'init_gap'
CONT_GAP = 'cont_gap'


class NeedlemanWunschConfiguration(AlignmentConfiguration):
    def __init__(self, current_directory, config):
        super().__init__(current_directory, config)

        # INPUT PARAMETERS
        ranges = self._config['ranges']

        # Calculate Maximum Acceptable Distance (MAD)
        self._mad = np.arange(
            ranges['mad']['start'],
            ranges['mad']['end'],
            ranges['mad']['step']
        )

        # Calculate Weight for Low complexity areas
        self._low = np.arange(
            ranges['low']['start'],
            ranges['low']['end'],
            ranges['low']['step']
        )

        # Calculate Weights for Affine Gap
        self._init_gap = np.arange(
            ranges['init_gap']['start'],
            ranges['init_gap']['end'],
            ranges['init_gap']['step']
        )

        self._cont_gap = np.arange(
            ranges['cont_gap']['start'],
            ranges['cont_gap']['end'],
            ranges['cont_gap']['step']
        )

    def _get_hyperparameters_labels(self) -> list:
        return [INIT_GAP, CONT_GAP, LOW, MAD]

    def _get_hyperparameters_ranges(self) -> list:
        return [self._init_gap, self._cont_gap, self._low, self._mad]

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            **super().get_config_params(pt_trace, dt_trace, current_config),
            **current_config
        }
