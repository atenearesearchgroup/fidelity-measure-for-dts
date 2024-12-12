from hyperparam_tuning.window.change_point.change_point_subject import ChangePointSubject
from hyperparam_tuning.window.stat_analysis.anomaly import AnomalyStatAnalysis as anst
from hyperparam_tuning.window.stat_analysis.iwindow import WindowStatAnalysis as wst
from hyperparam_tuning.window.stat_filters.iwindow import WindowStatsFilter as hsf
from util import generate_sublist_ranges
from util.file import generate_sublist_values


class AnomalyChangePointSubject(ChangePointSubject):
    def __init__(self, index_params, index_order_by, stat_filter):
        selected_params = generate_sublist_ranges(self._all_params,
                                                  index_params)
        order_by = generate_sublist_values(self._all_params,
                                           index_order_by)
        super().__init__(selected_params, order_by, stat_filter)

    @property
    def _all_params(self):
        return [
            wst.PERIOD,
            wst.DURATION,
            hsf.PERIOD_DIVIDE_DURATION,
            anst.INPUT_ANOMALY_LEN,
            anst.LEN_WINDOW_ANOMALY,
            wst.MIN_MS,
            wst.MAX_MS,
            wst.MEAN_MS,
            hsf.MAX_DROP_MS,
            hsf.MIN_DROP_MS
        ]
