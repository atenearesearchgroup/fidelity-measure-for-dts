import os

import numpy as np

from algorithm.config.alg_config import AlgorithmConfiguration
from batch.mode.imode import AlignmentMode
from result_analysis.window.graphics import generate_window_statistics


class WindowAlignmentMode(AlignmentMode):
    INTERVAL_DURATION = 'duration'
    INTERVAL_PERIOD = 'period'
    TS_START = 'ts_start'
    TS_END = 'ts_end'

    def __init__(self, config: AlgorithmConfiguration):
        super().__init__(config)
        self._align_folder = None
        self._interval_period = -1
        self._interval_duration = -1

    def execute_inner_alignments(self):
        self.create_alignments_folder()
        self._set_intervals()

        w_range = self._get_range(self._execution.dt_trace, self._execution.pt_trace)
        for w_end in w_range:
            dt_trace_w, pt_trace_w = self._get_subtrace(w_end,
                                                        self._execution.dt_trace,
                                                        self._execution.pt_trace)

            alignment_df, score, time_dict = self._execute_algorithm(dt_trace_w,
                                                                     pt_trace_w)

            time_window_dict = self._get_time_window(dt_trace_w, w_end)
            if self._config.align_files:
                self._export_alignment_results(alignment_df,
                                               dt_trace_w,
                                               pt_trace_w,
                                               os.path.join(self._execution.folder,
                                                            self._execution.get_filename(
                                                                extra=f"({time_window_dict[self.TS_START]},"
                                                                      f"{time_window_dict[self.TS_END]})")))

            self._execution.calculate_metrics(score, alignment_df, dt_trace_w, pt_trace_w,
                                              time_dict,
                                              extra_columns=time_window_dict)

        if w_range.shape[0] > 0:
            self._execution.export_metrics(self._get_metrics_filepath('.csv'))

            fig = generate_window_statistics(self._execution.dt_trace,
                                             self._execution.pt_trace,
                                             self._execution.results,
                                             self._config.param_interest,
                                             self._config.timestamp_label,
                                             self._execution.alg_current_config['mad'][
                                                 self._config.param_interest])
            fig.write_image(self._get_metrics_filepath('.pdf'), format="pdf",
                            engine=self._config.engine)

    def _get_time_window(self, dt_trace_w, w_end):
        return {
            'w_start': w_end - self._interval_duration,
            'w_end': w_end,
            self.TS_START: dt_trace_w[self._config.timestamp_label].iloc[0],
            self.TS_END: dt_trace_w[self._config.timestamp_label].iloc[-1]
        }

    def create_alignments_folder(self):
        self._scenario.create_folder()
        if self._config.align_files:
            self._execution.create_folder()

    def _get_metrics_filepath(self, extension):
        return os.path.join(self._scenario.folder,
                            self._execution.get_scenario_filename(extension))

    def _get_range(self, dt_trace, pt_trace):
        end = min(len(dt_trace), len(pt_trace))
        return np.arange(self._interval_duration, end, self._interval_period)

    def _set_intervals(self):
        self._interval_period = self._execution.alg_current_config[self.INTERVAL_PERIOD]
        self._interval_duration = self._execution.alg_current_config[self.INTERVAL_DURATION]
        self._execution.alg_current_config.pop(self.INTERVAL_PERIOD)
        self._execution.alg_current_config.pop(self.INTERVAL_DURATION)

    def _get_subtrace(self, w_end, dt_trace, pt_trace):
        w_start = w_end - self._interval_duration
        return dt_trace.iloc[w_start:w_end], pt_trace.iloc[w_start:w_end]
