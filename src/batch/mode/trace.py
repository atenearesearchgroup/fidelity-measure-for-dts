import os

from algorithm.config.alg_config import AlgorithmConfiguration
from batch.mode.imode import AlignmentMode


class TraceAlignmentMode(AlignmentMode):

    def __init__(self, config: AlgorithmConfiguration, trace_modifiers: list = []):
        super().__init__(config, trace_modifiers)
        self._create_metrics_folder()

    def execute_inner_alignments(self):
        alignment_df, score, time_dict = self._execute_algorithm(self._execution.dt_trace,
                                                                 self._execution.pt_trace)

        if self._config.align_files:
            self._export_alignment_results(alignment_df,
                                           self._execution.dt_trace,
                                           self._execution.pt_trace,
                                           os.path.join(self._config.output_directory,
                                                        self._execution.get_filename(
                                                            scenario=True)))

        self._execution.calculate_metrics(score, alignment_df, self._execution.dt_trace,
                                          self._execution.pt_trace, time_dict)
        self._execution.export_metrics(os.path.join(self._metrics_folder,
                                                    self._scenario.get_name(extension='.csv')))

    def _create_metrics_folder(self):
        self._metrics_folder = os.path.join(self._config.output_directory,
                                            'results')
        os.makedirs(self._metrics_folder, exist_ok=True)
