from batch_processing.alg_config.alignment_config import AlignmentConfiguration


class DynamicTimeWarpingSnapsConfig(AlignmentConfiguration):
    SYSTEM = 'system'
    TIMESTAMP_LABEL = 'timestamp_label'

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            **super().get_config_params(pt_trace, dt_trace, current_config),
            self.SYSTEM: self._system,
            self.TIMESTAMP_LABEL: self.timestamp_label,
            **current_config
        }
