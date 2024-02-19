"""
window.align
~~~~~~~~~~~~~~~~

This class performs an alignment of two traces and returns the resulting alignment and the
statistics as dataframes.
"""
import time

import pandas as pd

from algorithm.factory import AlignmentAlgorithmFactory
from batch.config.alg_config import AlgorithmConfiguration
from util.dic_util import nested_set


class WindowAlignments:
    """
    This class performs an alignment of two traces and returns the resulting alignment and the
    statistics as dataframes.
    """

    def __init__(self, config: AlgorithmConfiguration):
        self._config = config

    def execute_alignments(self, dt_trace, pt_trace):
        """
        It performs an alignment of two traces and returns the resulting alignment and the
        statistics as dataframes.
        :param dt_trace: Digital Twin trace
        :param pt_trace: Physical Twin trace
        :return: Alignment DataFrame, Statistical results DataFrame
        """
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
                                                                      pd.DataFrame.from_dict(
                                                                          dt_trace),
                                                                      pd.DataFrame.from_dict(
                                                                          pt_trace),
                                                                      current_config,
                                                                      alg.score),
                                 'execution_time': ex_time,
                                 'process_time': process_time,
                                 'trace_length': max(len(dt_trace), len(pt_trace))}

            statistical_results_df = pd.concat(
                [statistical_results_df,
                 pd.DataFrame.from_records([alignment_metrics])],
                ignore_index=True)

        print('alignment done!')
        return alignment_df, statistical_results_df
