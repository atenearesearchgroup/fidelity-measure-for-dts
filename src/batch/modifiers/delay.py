import random

from batch.modifiers.alter_trace import AlterTraceAlignmentWraper


class DelayWrapper(AlterTraceAlignmentWraper):
    LEN_DELAY = 'delay_len'

    def __init__(self):
        super().__init__(self.LEN_DELAY)

    def _alter_trace(self, len_modification, execution, config):
        len_values = execution.dt_trace.shape[0]
        upper_threshold = len_modification if len_values < len_modification else len_values - len_modification

        position = random.randrange(0, upper_threshold)

        result = execution.dt_trace.copy()
        for p in config.params:
            for i in range(len_modification):
                noise = random.uniform(-0.015, 0.015)
                result.loc[position + i, p] \
                    = execution.dt_trace.loc[position, p] + noise

            result.loc[position + len_modification:len_values, p] = \
                execution.dt_trace.loc[position + 1:len_values - len_modification + 1, p]

        return position, result
