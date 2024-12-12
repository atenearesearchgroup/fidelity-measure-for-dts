from hyperparam_tuning.window.stat_analysis.anomaly import AnomalyStatAnalysis as anst
from hyperparam_tuning.window.stat_analysis.iwindow import WindowStatAnalysis as wst
from hyperparam_tuning.window.stat_filters.iwindow import WindowStatsFilter


class AnomalyStatsFilter(WindowStatsFilter):
    MIN_DROP_MS = 'min_drop_ms'
    MAX_DROP_MS = 'max_drop_ms'
    HALF_INPUT_ANOMALY_LEN = f'half_{anst.INPUT_ANOMALY_LEN}'
    ODD_INPUT_ANOMALY_LEN = f'odd_{anst.INPUT_ANOMALY_LEN}'

    def apply_filters(self, df_filter):
        df_filter()
        self.insert_pe_divide_du()
        self.insert_max_drop()
        self.insert_min_drop()
        return self._stats_df

    def insert_min_drop(self):
        self._stats_df[self.HALF_INPUT_ANOMALY_LEN] = self._stats_df[anst.INPUT_ANOMALY_LEN] // 2
        self._stats_df[self.ODD_INPUT_ANOMALY_LEN] = self._stats_df[anst.INPUT_ANOMALY_LEN] % 2
        self._stats_df[self.MIN_DROP_MS] = (
                ((self._stats_df[wst.DURATION]) - (
                        self._stats_df[self.HALF_INPUT_ANOMALY_LEN]
                        + self._stats_df[self.ODD_INPUT_ANOMALY_LEN])) /
                (self._stats_df[wst.DURATION]))
        self._stats_df[self.MIN_DROP_MS] = (self._stats_df[self.MIN_DROP_MS].apply(
            lambda x: max(0, x))) * 100

    def insert_pe_divide_du(self):
        self._stats_df[self.PERIOD_DIVIDE_DURATION] = self._stats_df[wst.PERIOD] - self._stats_df[
            wst.DURATION]

    def insert_max_drop(self):
        self._stats_df[self.MAX_DROP_MS] = (
            (((self._stats_df[wst.DURATION]) - self._stats_df[anst.INPUT_ANOMALY_LEN]) /
             (self._stats_df[wst.DURATION])))
        self._stats_df[self.MAX_DROP_MS] = (self._stats_df[self.MAX_DROP_MS].apply(
            lambda x: max(0, x))) * 100

    def filter_anomaly_found(self):
        self._stats_df = self._stats_df[self._stats_df.apply(
            lambda x: x[anst.LEN_WINDOW_ANOMALY] > 0, axis=1)]

    def filter_anomaly_not_found(self):
        self._stats_df = self._stats_df[self._stats_df.apply(
            lambda x: x[anst.LEN_WINDOW_ANOMALY] <= 0, axis=1)]
