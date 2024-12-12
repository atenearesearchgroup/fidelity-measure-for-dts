from hyperparam_tuning.window.change_point.anomaly import AnomalyChangePointSubject
from hyperparam_tuning.window.stat_analysis.iwindow import WindowStatAnalysis as wst


class DelayChangePointSubject(AnomalyChangePointSubject):

    @property
    def _all_params(self):
        return [
            wst.PERIOD,
            wst.DURATION,
            'de_len',
            f'{wst.MIN_MS}_bf',
            f'{wst.MIN_MS}_af',
            f'{wst.MAX_MS}_bf',
            f'{wst.MAX_MS}_af',
            f'{wst.MEAN_MS}_bf',
            f'{wst.MEAN_MS}_af',
            f'{wst.STD_MS}_bf',
            f'{wst.STD_MS}_af',
        ]
