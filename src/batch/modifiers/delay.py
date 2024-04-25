import random

from batch.modifiers.alter_trace import AlterTraceAlignmentWraper


class DelayWrapper(AlterTraceAlignmentWraper):
    LEN_DELAY = 'len_delay'

    def alter_trace(self, execution, config):
        len_delay = execution.alg_current_config[self.LEN_DELAY]
        execution.alg_current_config.pop(self.LEN_DELAY)

        len_values = execution.dt_trace.shape[0]
        upper_threshold = len_delay if len_values < len_delay else len_values - len_delay
        position = random.randrange(0, upper_threshold)

        result = execution.dt_trace.copy()
        for i in range(len_delay):
            noise = random.uniform(-0.015, 0.015)
            result.iloc[position + i, 1] \
                = execution.dt_trace.iloc[position, 1] + noise

        result.iloc[position + len_delay:len_values, 1] = \
            execution.dt_trace.iloc[position + 1:len_values - len_delay + 1, 1]

        start = execution.dt_trace[config.timestamp_label][position]
        end = execution.dt_trace[config.timestamp_label][position + len_delay]
        return {'delay': f'({start},{end})'}
