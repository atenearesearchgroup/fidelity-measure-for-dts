from abc import ABC, abstractmethod

import plotly.io as pio

import util.file as fu
from algorithm.config.alg_config import AlgorithmConfiguration
from algorithm.logic.factory import AlignmentAlgorithmFactory
from batch.scenario import Scenario
from graphics.alignment.factory import GraphicFactory
from util.timing import timing

pio.kaleido.scope.mathjax = None


class AlignmentMode(ABC):

    def __init__(self, config: AlgorithmConfiguration):
        self._config = config
        self._scenario = None
        self._execution = None
        self._trace_modifiers = []

    def add_trace_modifier(self, modifier):
        self._trace_modifiers.append(modifier)

    def execute_alignments(self):
        """
        This method performs a set of alignments for a given algorithm.
        The resulting alignments can be exported as CSV files, with optional PDF images, and
        statistical metrics are also exported as CSV files.
        """
        for i, starting_pattern in enumerate(self._config.pt_files):
            for pt_file in fu.list_directory_files(self._config.pt_path, '.csv', starting_pattern):
                self._scenario = Scenario(self._config, pt_file, self._config.dt_files[i])

                for curr_config_tuple in self._config.get_hyperparameters_combinations():
                    self._execution = self._scenario.create_execution(curr_config_tuple)

                    self.apply_trace_modifiers()
                    self.execute_inner_alignments()

    def apply_trace_modifiers(self):
        for alter in self._trace_modifiers:
            modifier_position = alter.alter_trace(self._execution, self._config)
            self._execution.params_dict.update(modifier_position)

    def _execute_algorithm(self, dt_trace_w, pt_trace_w):
        @timing
        def _perform_alignment(current_config, dt_trace_w, pt_trace_w):
            alg = AlignmentAlgorithmFactory. \
                get_alignment_algorithm(self._config.alignment_algorithm,
                                        **self._config.get_config_params(
                                            pt_trace_w,
                                            dt_trace_w,
                                            current_config))
            return alg.calculate_alignment(), alg.score

        alg, alignment_df, time_dict = _perform_alignment(self._execution.alg_current_config,
                                                          dt_trace_w, pt_trace_w)
        print(f"--- SCENARIO: {self._scenario.get_name()} ---")
        print(f"---{self._execution.get_scenario_filename(extension='')}"
              f" : {time_dict['clock_time'] :.2f} seconds"
              f" : {time_dict['process_time'] :.2f} seconds ---")
        return alg, alignment_df, time_dict

    def _generate_graphics(self, alignment_df, dt_trace, pt_trace, output_filepath):
        """
        Exports the alignment figure to pdf
        :param alignment_df: Dataframe with the resulting alignment
        :param dt_trace: Digital Twin Trace
        :param pt_trace: Physical Twin Trace
        :param output_filepath: Output filepath for the figure
        """
        if self._config.figures:
            fig = GraphicFactory.get_graphic(self._config.alignment_algorithm, alignment_df,
                                             dt_trace, pt_trace,
                                             **{'params_of_interest': self._config.params,
                                                'timestamp_label': self._config.timestamp_label,
                                                'visualization_indent': self._config.visualization_indent})
            height = 600 if len(self._config.params) == 1 else 950
            width = 1400 if len(self._config.params) == 1 else 1400
            fig.write_image(output_filepath.replace(".csv", ".pdf"), format="pdf", width=width,
                            height=height,
                            engine=self._config.engine)

    def _export_alignment_results(self, alignment_df, dt_trace_w, pt_trace_w, filepath):
        if not alignment_df.empty:
            alignment_df.to_csv(filepath, index=False, encoding='utf-8', sep=',')

            self._generate_graphics(alignment_df, dt_trace_w, pt_trace_w,
                                    filepath)

    @abstractmethod
    def execute_inner_alignments(self):
        pass

    def _get_traces(self):
        return self._execution.dt_trace, self._execution.pt_trace
