from batch_processing.alg_config.alignment_config import AlignmentConfiguration


class DynamicTimeWarpingLugaresiConfig(AlignmentConfiguration):
    PARAM_INTEREST = 'param_interest'

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            **super().get_config_params(pt_trace, dt_trace, current_config),
            self.PARAM_INTEREST: self._param_interest,
            **current_config
        }
