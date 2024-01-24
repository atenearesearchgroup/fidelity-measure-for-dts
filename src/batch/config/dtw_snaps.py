"""
batch.config.dtw_snaps
~~~~~~~~~~~~~~~~

A class that generates alignment batches for the adaptation of Dynamic Time Warping adapted to
enable the alignment of snapshot sequences. It takes the batch configuration from a YAML file,
including input ranges and configuration parameters.
"""
from batch.config.alg_config import AlgorithmConfiguration


class DynamicTimeWarpingSnapsConfig(AlgorithmConfiguration):
    """
    A class that generates alignment batches for the adaptation of Dynamic Time Warping adapted to
    enable the alignment of snapshot sequences. It takes the batch configuration from a YAML file,
    including input ranges and configuration parameters.
    """

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
            AlgorithmConfiguration.SYSTEM: self._system,
            AlgorithmConfiguration.TIMESTAMP_LABEL: self.timestamp_label
        }
