import os
import time

import pandas as pd

import util.file_util as fu
from algorithm.algorithm_factory import AlignmentAlgorithmFactory
from batch_processing import AlignmentConfiguration
from result_analysis.alignment_graphic.graphic_factory import GraphicFactory
from util.dic_util import nested_set
from util.file_util import generate_filename


class BatchAlignments:
    def __init__(self, config: AlignmentConfiguration):
        self._config = config

    def execute_alignments(self):
        for i, starting_pattern in enumerate(self._config.pt_files):
            for pt_file in fu.list_directory_files(self._config.pt_path, '.csv', starting_pattern):
                scenario = self._config.get_scenario(self._config.dt_file[i], pt_file)
                global_results_filename = scenario + '.csv'

                # DT and PT traces in dict with only the parameters of interest
                dt_trace = pd.read_csv(self._config.dt_path + self._config.dt_file[i]) \
                    .filter(items=[self._config.timestamp_label, *self._config.params])
                pt_trace = pd.read_csv(self._config.pt_path + pt_file) \
                    .filter(items=[self._config.timestamp_label, *self._config.params])

                statistical_results_df = pd.DataFrame()
                for init_config in self._config.get_hyperparameters_combinations():
                    current_config = {}
                    for index, label in enumerate(self._config.get_hyperparameters_labels()):
                        nested_set(current_config, label.split('-'), init_config[index])

                    alignment_filepath = os.path. \
                        join(self._config.output_directory,
                             f"{scenario}-{generate_filename(current_config)}.csv")

                    start_ex_time = time.time()
                    start_proc_time = time.process_time()

                    alg = AlignmentAlgorithmFactory. \
                        get_alignment_algorithm(self._config.alignment_algorithm,
                                                **self._config.get_config_params(
                                                    pt_trace.to_dict('records'),
                                                    dt_trace.to_dict('records'),
                                                    current_config))

                    alignment_df = alg.calculate_alignment()

                    process_time = time.process_time() - start_proc_time
                    ex_time = time.time() - start_ex_time

                    print(f"--- SCENARIO: {scenario} ---")
                    print(f"---{generate_filename(current_config)}"
                          f" : {process_time :.2f} seconds ---")

                    if not alignment_df.empty:
                        alignment_df.to_csv(alignment_filepath, index=False,
                                            encoding='utf-8', sep=',')

                        if self._config.figures:
                            # --- GRAPHIC GENERATION ---
                            fig = GraphicFactory.get_graphic(self._config.alignment_algorithm,
                                                             alignment_df,
                                                             dt_trace,
                                                             pt_trace,
                                                             **{'params_of_interest':
                                                                    self._config.params,
                                                                'timestamp_label':
                                                                    self._config.timestamp_label})
                            height = 800
                            if len(self._config.params) > 1:
                                height = 3000
                            fig.write_image(alignment_filepath.replace(".csv", ".pdf"),
                                            format="pdf", width=2500, height=height,
                                            engine=self._config.engine)
                            # fig.show()

                    alignment_metrics = {**self._config.get_alignment_metrics(alignment_df,
                                                                              dt_trace,
                                                                              pt_trace,
                                                                              current_config,
                                                                              alg.score),
                                         'execution_time': ex_time,
                                         'process_time': process_time,
                                         'trace_length': max(len(dt_trace), len(pt_trace))}

                    statistical_results_df = pd.concat(
                        [statistical_results_df,
                         pd.DataFrame.from_records([alignment_metrics])],
                        ignore_index=True)

                output_path = os.path.join(self._config.output_results_directory,
                                           global_results_filename)

                statistical_results_df.to_csv(output_path, mode='a',
                                              header=not os.path.exists(output_path),
                                              index=False)
