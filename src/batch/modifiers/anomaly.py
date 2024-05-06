import random

from batch.modifiers.alter_trace import AlterTraceAlignmentWraper


class AnomalyWrapper(AlterTraceAlignmentWraper):
    MAD = 'mad'
    ANOMALY = 'anomaly'

    def __init__(self):
        super().__init__(self.ANOMALY)

    def _alter_trace(self, len_modification, execution, config, pos_modification):
        mad = execution.alg_current_config[self.MAD]

        result = execution.dt_trace.copy()
        if pos_modification < 0:
            pos_modification = random.randrange(0, execution.dt_trace.shape[0] - len_modification)

        for p in config.params:
            mad_threshold = mad[p] * 2
            column = execution.dt_trace[p]
            max_value = column.max()
            min_value = column.min()
            lower_threshold = min_value if min_value > mad_threshold else mad_threshold

            for i in range(len_modification):
                offset = random.choice([-1, 1]) * random.uniform(lower_threshold, max_value)
                result.loc[pos_modification + i, p] = column.iloc[pos_modification + i] + offset

        return pos_modification, result
