import logging

import numpy as np
import pandas as pd

from batch.mode.window import WindowAlignmentMode as w
from hyperparam_tuning.window.stat_analysis.iwindow import WindowStatAnalysis
from util.dataframe import is_subset


class AnomalyStatAnalysis(WindowStatAnalysis):
    INPUT_ANOMALY_LEN = 'an_len'
    LEN_WINDOW_ANOMALY = 'len_anomaly'

    def get_statistics(self, metrics: pd.DataFrame):
        percentage_ms = metrics[self.P_MS] if not metrics.empty else pd.Series()
        return {
            **self.values,
            self._modifier_len: len(metrics),
            self.MIN_MS: percentage_ms.min(),
            self.MAX_MS: percentage_ms.max(),
            self.MEAN_MS: percentage_ms.mean(),
            self.STD_MS: percentage_ms.std()
        }

    def calculate_statistics(self, filename: str, result: pd.DataFrame):
        anomaly_detected = False
        groups_indexes = iter(self._get_anomalous_window_groups_indexes().values())
        while (group_index := next(groups_indexes, None)) is not None and not anomaly_detected:
            group_values = self.metrics.loc[group_index[0]:group_index[-1]]
            anomaly_detected = is_subset(self._get_artificial_anomaly(), group_values)
            if anomaly_detected:
                logging.info('-- Processing %s --', filename)
                result = self._append_statistics(result, group_values)
        if not anomaly_detected:
            logging.debug('-- Anomaly not detected for file %s --', filename)
            result = self._append_statistics(result, pd.DataFrame())
        return result

    def _filter_artificial_anomalous_range(self, input_df):
        return input_df[
            (
                    (
                            (input_df[w.TS_START] >= self._values[self._modifier_pos][0]) &
                            (input_df[w.TS_START] <= self._values[self._modifier_pos][1])
                    ) |
                    (
                            (input_df[w.TS_END] >= self._values[self._modifier_pos][0]) &
                            (input_df[w.TS_END] <= self._values[self._modifier_pos][1])
                    ) |
                    (
                            (input_df[w.TS_START] <= self._values[self._modifier_pos][0]) &
                            (input_df[w.TS_END] >= self._values[self._modifier_pos][1])
                    )
            )
        ]

    def _calculate_iqr_boundaries(self, data):
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)

        iqr = q3 - q1

        return q1 - 1.5 * iqr, q3 + 1.5 * iqr

    def _get_anomalous_windows(self):
        q1, q3 = self._calculate_iqr_boundaries(self._metrics[self.P_MS])
        return self._metrics[(self._metrics[self.P_MS] < q1) |
                             (self._metrics[self.P_MS] > q3)]

    def _get_artificial_anomaly(self):
        return self._filter_artificial_anomalous_range(
            self._get_anomalous_windows())

    def _get_anomalous_window_groups_indexes(self):
        all_anomalous_windows = self._get_anomalous_windows()
        all_anomalous_windows = all_anomalous_windows.assign(group_col=all_anomalous_windows.index)
        g = pd.DataFrame(all_anomalous_windows['group_col'].diff().gt(1).cumsum())
        g.loc[:, 'index_col'] = g.index
        return g.groupby('group_col').agg(list).to_dict()['index_col']
