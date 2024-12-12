from abc import abstractmethod, ABC

from hyperparam_tuning.window.stat_analysis.iwindow import WindowStatAnalysis as wst


class WindowStatsFilter(ABC):
    MIN_DROP_MS = 'min_drop_ms'
    MAX_DROP_MS = 'max_drop_ms'
    PERIOD_DIVIDE_DURATION = f'{wst.PERIOD}/{wst.DURATION}'

    def __init__(self, stats_df):
        self._stats_df = stats_df

    @abstractmethod
    def apply_filters(self, df_filter):
        pass

    def filter_period_equals_duration(self):
        self._stats_df = self._stats_df[self._stats_df.apply(
            lambda x: x[wst.PERIOD] == x[wst.DURATION], axis=1)]

    def filter_period_greater_duration(self):
        self._stats_df = self._stats_df[self._stats_df.apply(
            lambda x: x[wst.PERIOD] > x[wst.DURATION], axis=1)]

    def filter_period_less_duration(self):
        self._stats_df = self._stats_df[self._stats_df.apply(
            lambda x: x[wst.PERIOD] < x[wst.DURATION], axis=1)]

    @property
    def stats_df(self):
        return self._stats_df

    @stats_df.setter
    def stats_df(self, value):
        self._stats_df = value
