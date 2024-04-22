import random

from batch.wrapper.alter_trace import AlterTraceAlignmentWraper


class DelayWrapper(AlterTraceAlignmentWraper):
    LEN_DELAY = 'len_delay'

    def _alter_trace(self, current_config, trace, params=None):
        self._set_random_seed()
        len_delay = current_config[self.LEN_DELAY]
        current_config.pop(self.LEN_DELAY)

        len_values = trace.shape[0]
        upper_threshold = len_delay if len_values < len_delay else len_values - len_delay
        position = random.randrange(0, upper_threshold)

        result = trace.copy()
        for i in range(len_delay):
            noise = random.uniform(-0.015, 0.015)
            result.iloc[position + i, 1] \
                = trace.iloc[position, 1] + noise

        result.iloc[position + len_delay:len_values, 1] = \
            trace.iloc[position + 1:len_values - len_delay + 1, 1]

        start = trace[self._config.timestamp_label][position]
        end = trace[self._config.timestamp_label][position + len_delay]
        return result, {'delay': f'({start},{end})'}
