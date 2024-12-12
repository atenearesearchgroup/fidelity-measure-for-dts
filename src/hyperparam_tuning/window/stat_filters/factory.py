from batch.modifiers.anomaly import AnomalyWrapper as an
from batch.modifiers.delay import DelayWrapper as de
from hyperparam_tuning.window.stat_filters.anomaly import AnomalyStatsFilter
from hyperparam_tuning.window.stat_filters.delay import DelayStatFilters


class StatFiltersFactory:
    @staticmethod
    def get_filters(modifier, stats_df):
        modifiers = {
            de.DELAY: DelayStatFilters,
            an.ANOMALY: AnomalyStatsFilter
        }
        if modifier in modifiers:
            return modifiers[modifier](stats_df)
        raise ValueError(f'Invalid input modifier name {modifier}.')
