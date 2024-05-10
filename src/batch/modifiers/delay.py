import random

from batch.modifiers.alter_trace import AlterTraceAlignmentWraper


class DelayWrapper(AlterTraceAlignmentWraper):
    DELAY = 'delay'

    def __init__(self):
        super().__init__(self.DELAY)

    def _alter_trace(self, len_modification, execution, config, pos_modification):
        len_values = execution.dt_trace.shape[0]

        if pos_modification < 0:
            upper_threshold = len_modification if len_values < len_modification else len_values - len_modification
            pos_modification = random.randrange(0, upper_threshold)

        result = execution.dt_trace.copy()
        for param_i, p in enumerate(config.params, 1):
            for i in range(len_modification):
                noise = random.uniform(-0.015, 0.015)
                result.iloc[pos_modification + i, param_i] \
                    = execution.dt_trace.iloc[pos_modification, param_i] + noise

            result.iloc[pos_modification + len_modification:len_values - 1, param_i] = \
                execution.dt_trace.iloc[pos_modification + 1:len_values - len_modification, param_i]

        return pos_modification, result
