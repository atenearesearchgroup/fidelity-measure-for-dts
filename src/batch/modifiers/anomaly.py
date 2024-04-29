import random

from batch.modifiers.alter_trace import AlterTraceAlignmentWraper


class AnomalyWrapper(AlterTraceAlignmentWraper):
    MAD = 'mad'
    LEN_ANOMALY = 'anomaly_len'

    def __init__(self):
        super().__init__(self.LEN_ANOMALY)

    def _alter_trace(self, len_modification, execution, config):
        mad = execution.alg_current_config[self.MAD]

        result = execution.dt_trace.copy()
        position = -1
        for p in config.params:
            mad_threshold = mad[p] * 2
            column = execution.dt_trace[p]
            max_value = column.max()
            min_value = column.min()
            lower_threshold = min_value if min_value > mad_threshold else mad_threshold

            position = random.randrange(0, execution.dt_trace.shape[0] - len_modification)

            for i in range(len_modification):
                offset = random.choice([-1, 1]) * random.uniform(lower_threshold, max_value)
                result.loc[position + i, p] = column.iloc[position + i] + offset

        return position, result
