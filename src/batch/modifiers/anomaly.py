import random

from batch.modifiers.alter_trace import AlterTraceAlignmentWraper


class AnomalyWrapper(AlterTraceAlignmentWraper):
    MAD = 'mad'
    LEN_ANOMALY = 'len_anomaly'

    def alter_trace(self, execution, config):
        mad = execution.alg_current_config[self.MAD]
        len_anomaly = execution.alg_current_config[self.LEN_ANOMALY]
        execution.alg_current_config.pop(self.LEN_ANOMALY)

        result = execution.dt_trace.copy()
        position = -1
        for p in config.params:
            mad_threshold = mad[p] * 2
            column = execution.dt_trace[p]
            max_value = column.max()
            min_value = column.min()
            lower_threshold = min_value if min_value > mad_threshold else mad_threshold

            position = random.randrange(0, execution.dt_trace.shape[0] - len_anomaly)

            for i in range(len_anomaly):
                offset = random.uniform(lower_threshold, max_value)
                result.loc[position + 1, p] = column.iloc[position + 1] + offset

        start = execution.dt_trace[config.timestamp_label][position]
        end = execution.dt_trace[config.timestamp_label][position + len_anomaly]
        return {'anomaly': f'({start},{end})'}
