import random

from batch.wrapper.alter_trace import AlterTraceAlignmentWraper


class AnomalyWrapper(AlterTraceAlignmentWraper):
    MAD = 'mad'
    LEN_ANOMALY = 'len_anomaly'

    def _alter_trace(self, current_config, trace, params=None):
        self._set_random_seed()
        mad = current_config[self.MAD]
        len_anomaly = current_config[self.LEN_ANOMALY]
        current_config.pop(self.LEN_ANOMALY)

        result = trace.copy()
        position = -1
        for p in params:
            mad_threshold = mad[p] * 2
            column = trace[p]
            max_value = column.max()
            min_value = column.min()
            lower_threshold = min_value if min_value > mad_threshold else mad_threshold

            position = random.randrange(0, trace.shape[0] - len_anomaly)

            for i in range(len_anomaly):
                offset = random.uniform(lower_threshold, max_value)
                result.loc[position + 1, p] = column.iloc[position + 1] + offset

        start = trace[self._config.timestamp_label][position]
        end = trace[self._config.timestamp_label][position + len_anomaly]
        return result, {'anomaly': f'({start},{end})'}
