import logging

import pandas as pd

from batch.mode.window import WindowAlignmentMode as w
from hyperparam_tuning.window.stat_analysis.iwindow import WindowStatAnalysis


class DelayStatAnalysis(WindowStatAnalysis):
    def get_statistics(self, metrics: pd.DataFrame):
        after_percentage_ms = self._filter_delayed_range(metrics)[
            self.P_MS] if not metrics.empty else pd.Series()
        before_percentage_ms = self._filter_non_delayed_range(metrics)[
            self.P_MS] if not metrics.empty else pd.Series()
        if not (after_percentage_ms.empty or before_percentage_ms.empty):
            return {
                **self.values,
                **{
                    self._stat_label_before(key): func(before_percentage_ms) for key, func in
                    self._stat_labels.items()
                },
                **{
                    self._stat_label_after(key): func(after_percentage_ms) for key, func in
                    self._stat_labels.items()
                }
            }
        return {}

    def _stat_label_before(self, stat_label):
        return f'{stat_label}_bf'

    def _stat_label_after(self, stat_label):
        return f'{stat_label}_af'

    def _stat_label_diff(self, stat_label):
        return f'{stat_label}_diff'

    @property
    def _stat_labels(self):
        return {self.MIN_MS: lambda df: df.min(),
                self.MAX_MS: lambda df: df.max(),
                self.MEAN_MS: lambda df: df.mean(),
                self.STD_MS: lambda df: df.std()}

    def _filter_delayed_range(self, input_df):
        return input_df[input_df[w.TS_START] >= self._values[self._modifier_pos][0]]

    def _filter_non_delayed_range(self, input_df):
        return input_df[input_df[w.TS_START] < self._values[self._modifier_pos][0]]

    def calculate_statistics(self, filename: str, result: pd.DataFrame):
        logging.info('-- Processing %s --', filename)
        result = self._append_statistics(result, self.metrics)
        return result
