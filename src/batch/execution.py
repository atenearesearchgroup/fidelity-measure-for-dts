import os

import pandas as pd

import util.file as fu
from metrics.metrics_factory import AnalysisFactory
from util.dict_util import dict_to_str, tuple_to_dict


class Execution():
    def __init__(self, scenario, current_config_tuple):
        self.folder = None
        self._scenario = scenario

        self.dt_trace = self._scenario.dt_trace.copy()
        self.pt_trace = self._scenario.pt_trace.copy()

        self.alg_current_config = tuple_to_dict(
            self._scenario.alg_config.get_hyperparameters_labels(),
            current_config_tuple)

        self._group_by_dict = {label: self.alg_current_config[label] for label in
                               self._scenario.alg_config.group_by}

        self.params_dict = {k: self.alg_current_config[k] for k in
                            set(self.alg_current_config) - set(self._group_by_dict)}

        self.results = pd.DataFrame()

    def calculate_metrics(self, score, alignment_df, dt_trace_w, pt_trace_w, time_dict,
                          extra_columns=None):
        if extra_columns is None:
            extra_columns = {}
        alignment_metrics = {**extra_columns,
                             **self._get_alignment_metrics(alignment_df,
                                                           dt_trace_w,
                                                           pt_trace_w,
                                                           score),
                             **time_dict,
                             'trace_length': max(len(dt_trace_w), len(pt_trace_w))}
        self._add_metrics_result(alignment_metrics)

    def export_metrics(self, output_path):
        self.results.to_csv(output_path, mode='a',
                            header=not os.path.exists(output_path),
                            index=False)

    def _get_alignment_metrics(self, alignment_df, dt_trace_w, pt_trace_w, score):
        """
        This method returns a dictionary containing the alignment input parameters and
        corresponding alignment metrics.

        :param alignment_df: Dataframe that contains the resulting alignment
        :param pt_trace: The Physical Twin trace
        :param dt_trace: The Digital Twin trace
        :param input_parameters: dictionary that contains the algorithm configuration parameters
        :param score: algorithm resulting score
        :return:
        """
        alg = self._scenario.alg_config
        alignment_results = AnalysisFactory.create_instance(alg.alignment_algorithm,
                                                            alg.lca,
                                                            alignment=alignment_df,
                                                            dt_trace=dt_trace_w,
                                                            pt_trace=pt_trace_w,
                                                            system=alg.system,
                                                            selected_params=alg.params,
                                                            score=score,
                                                            timestamp_label=alg.timestamp_label)

        statistical_values = fu.get_property_values(alignment_results, alg.methods)
        return {**fu.flatten_dictionary(self.alg_current_config),
                **fu.flatten_dictionary(statistical_values)}

    def _add_metrics_result(self, metrics_dict):
        self.results = pd.concat([self.results, pd.DataFrame.from_records([metrics_dict])],
                                 ignore_index=True)

    def get_name(self):
        return dict_to_str(self.alg_current_config)

    def get_filename(self, extra='', scenario=False, extension='.csv'):
        return f"{self._scenario.get_name() if scenario else ''}" \
               f"{dict_to_str(self.params_dict)}" \
               f"{'-' if extra else ''}" \
               f"{extra}" \
               f"{extension}"

    def get_scenario_filename(self, extension='.csv'):
        return f"{dict_to_str(self._group_by_dict)}__" \
               f"{dict_to_str(self.params_dict)}" \
               f"{extension}"

    def create_folder(self):
        if self._scenario.alg_config.group_by:
            self.folder = os.path.join(self._scenario.folder,
                                       dict_to_str(self._group_by_dict))
            os.makedirs(self.folder, exist_ok=True)
        else:
            self.folder = self._scenario.folder
