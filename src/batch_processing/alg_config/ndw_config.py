import numpy as np

from batch_processing.alg_config.alignment_config import AlignmentConfiguration


class NeedlemanWunschConfiguration(AlignmentConfiguration):
    MAD = 'mad'
    LOW = 'low'
    INIT_GAP = 'init_gap'
    CONT_GAP = 'cont_gap'
    SYSTEM = 'system'
    TIMESTAMP_LABEL = 'timestamp_label'

    def __init__(self, current_directory, args, config):
        super().__init__(current_directory, args, config)

        # INPUT PARAMETERS
        ranges = self.config['ranges']

        # Calculate Maximum Acceptable Distance (MAD)
        self._mad = {}
        mad = ranges['mad']
        for p in self.params:
            if p in mad:
                self._mad[p] = np.arange(
                    mad[p]['start'],
                    mad[p]['end'],
                    mad[p]['step']
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

    def get_hyperparameters_labels(self) -> list:
        return [self.INIT_GAP, self.CONT_GAP, self.LOW,
                *[f"{self.MAD}-{p}" for p in self._mad.keys()]]

    def _get_hyperparameters_ranges(self) -> list:
        return [self._init_gap, self._cont_gap, self._low, *self._mad.values()]

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            **super().get_config_params(pt_trace, dt_trace, current_config),
            self.SYSTEM: self._system,
            self.TIMESTAMP_LABEL: self.timestamp_label,
            **current_config
        }
