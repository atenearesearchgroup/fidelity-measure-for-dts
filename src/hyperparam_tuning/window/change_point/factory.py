from batch.modifiers.anomaly import AnomalyWrapper as an
from batch.modifiers.delay import DelayWrapper as de
from hyperparam_tuning.window.change_point.anomaly import AnomalyChangePointSubject
from hyperparam_tuning.window.change_point.delay import DelayChangePointSubject


class ChangePointFactory:
    @staticmethod
    def get_change_point(modifier, index_params, index_order_by, stat_filter):
        modifiers = {
            de.DELAY: DelayChangePointSubject,
            an.ANOMALY: AnomalyChangePointSubject
        }
        if modifier in modifiers:
            return modifiers[modifier](index_params, index_order_by, stat_filter)
        raise ValueError(f'Invalid input modifier name {modifier}.')
