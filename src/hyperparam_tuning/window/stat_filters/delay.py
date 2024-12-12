from hyperparam_tuning.window.stat_filters.iwindow import WindowStatsFilter


class DelayStatFilters(WindowStatsFilter):
    def apply_filters(self, df_filter):
        df_filter()
        return self._stats_df
