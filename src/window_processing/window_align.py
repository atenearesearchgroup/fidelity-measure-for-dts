import time

import pandas as pd

from batch_processing import AlignmentConfiguration
from algorithm.algorithm_factory import AlignmentAlgorithmFactory
from util.dic_util import nested_set


class WindowAlignments:
    def __init__(self, config: AlignmentConfiguration):
        self._config = config

    def execute_alignments(self, dt_trace, pt_trace):
        alignment_df = pd.DataFrame()
        statistical_results_df = pd.DataFrame()

        for init_config in self._config.get_hyperparameters_combinations():
            current_config = {}
            for index, label in enumerate(self._config.get_hyperparameters_labels()):
                nested_set(current_config, label.split('-'), init_config[index])

            start_ex_time = time.time()
            start_proc_time = time.process_time()

            alg = AlignmentAlgorithmFactory. \
                get_alignment_algorithm(self._config.alignment_algorithm,
                                        **self._config.get_config_params(
                                            pt_trace,
                                            dt_trace,
                                            current_config))

            alignment_df = alg.calculate_alignment()

            process_time = time.process_time() - start_proc_time
            ex_time = time.time() - start_ex_time

            alignment_metrics = {**self._config.get_alignment_metrics(alignment_df,
                                                                      pd.DataFrame.from_dict(dt_trace),
                                                                      pd.DataFrame.from_dict(pt_trace),
                                                                      current_config,
                                                                      alg.score),
                                 'execution_time': ex_time,
                                 'process_time': process_time,
                                 'trace_length': max(len(dt_trace), len(pt_trace))}

            statistical_results_df = pd.concat(
                [statistical_results_df,
                 pd.DataFrame.from_records([alignment_metrics])],
                ignore_index=True)

        print(f'alignment done!')
        return alignment_df, statistical_results_df
