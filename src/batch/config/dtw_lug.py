"""
batch.config.dtw_lug
~~~~~~~~~~~~~~~~

A class that generates alignment batches for the adaptation of Dynamic Time Warping presented by
Lugaresi et al. in [1]. It takes the batch configuration from a YAML file, including input ranges
and configuration parameters.

References:
    [1] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
    Online validation of digital twins for manufacturing systems. Comput.
    Ind. 150: 103942 (2023)
"""
from batch.config.alg_config import AlgorithmConfiguration


class DynamicTimeWarpingLugaresiConfig(AlgorithmConfiguration):
    """
    A class that generates alignment batches for the adaptation of Dynamic Time Warping presented by
    Lugaresi et al. in [1]. It takes the batch configuration from a YAML file, including input
    ranges and configuration parameters.

    References:
        [1] Giovanni Lugaresi, Sofia Gangemi, Giulia Gazzoni, Andrea Matta:
        Online validation of digital twins for manufacturing systems. Comput.
        Ind. 150: 103942 (2023)
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
            AlgorithmConfiguration.PARAM_INTEREST: self._param_interest
        }
