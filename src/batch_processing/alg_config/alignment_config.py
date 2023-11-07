import itertools
import os
import time

import pandas as pd

import util.file_util as fu
from batch_processing.algorithm_factory import AlignmentAlgorithmFactory
from batch_processing.analysis_factory import AnalysisFactory
from systems import Lift, SystemBase
from util.file_util import generate_filename

PT_TRACE = 'pt_trace'
DT_TRACE = 'dt_trace'
SYSTEM = 'system'
TIMESTAMP_LABEL = 'timestamp_label'


class AlignmentConfiguration:
    """
    This class parses a YAML file to generate alignment batches based on specified input ranges
    and configuration parameters for a sequence alignment algorithm.

    Attributes:
        - current_directory (str): Path to the current working directory, to use relative paths
        - args (dict): input command-line arguments
    """

    def __init__(self, current_directory, config):
        self._current_directory = current_directory
        self._config = config
        self._set_file_paths()
        self._initialize_analysis_labels()
        self._initialize_system()
        self._create_output_directories()

        # Set iterator pointer value
        self._iterator = 0

    def _set_file_paths(self):
        """
        Access the YAML-parsed information and set the file paths for the input sequence files.
        """
        paths = self._config['paths']
        inputs = paths['input']

        # FILE PATHS
        self._input_directory = os.path.join(self._current_directory, inputs['main'])
        self._output_directory = os.path.join(self._current_directory, paths['output'])

        # DIGITAL TWIN
        self._dt_path = os.path.join(self._input_directory, inputs['dt'])
        self._dt_file = inputs['dt_files']

        # PHYSICAL TWIN
        self._pt_path = os.path.join(self._input_directory, inputs['pt'])
        self._pt_files = inputs['pt_files']

    def _initialize_analysis_labels(self):
        """
        Access the YAML-parsed information and set the properties of interest labels.
        """
        labels = self._config['labels']

        self._timestamp_label = labels.get('timestamp_label', 'timestamp(s)')
        self._param_interest = labels['param_interest']
        self._params = labels['params']

    def _initialize_system(self):
        """
        Access the YAML-parsed information and initialize the set of methods for the output
        headers and the System object for the alignment.
        """
        system_name = self._config.get('system', 'System')
        self._system = Lift() if system_name == 'Lift' else SystemBase()

        self._lca = self._config.get('low_complexity_area', False)

        self._alignment_algorithm = self._config['alignment_alg']
        self._methods = fu.get_property_methods(AnalysisFactory.get_class
                                                (self._alignment_algorithm, self._lca))

    def _create_output_directories(self):
        """
            Create directories for storing individual result statistics and batch statistics.
        """
        self._output_results_directory = os.path.join(self._output_directory, 'results')
        directories = [self._output_directory, self._output_results_directory]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def execute_alignments(self):
        for i, starting_pattern in enumerate(self._pt_files):
            for pt_file in fu.list_directory_files(self._pt_path, '.csv', starting_pattern):
                scenario = self._get_scenario(self._dt_file[i], pt_file)
                global_results_filename = scenario + '.csv'

                # DT and PT traces in dict with only the parameters of interest
                dt_trace = pd.read_csv(self._dt_path + self._dt_file[i]) \
                    .filter(items=[self._timestamp_label, *self._params])
                pt_trace = pd.read_csv(self._pt_path + pt_file) \
                    .filter(items=[self._timestamp_label, *self._params])

                statistical_results_df = pd.DataFrame()
                for current_config in self._get_hyperparameters_combinations():
                    current_config = dict(zip(self._get_hyperparameters_labels(), current_config))

                    alignment_filepath = os.path. \
                        join(self._output_directory,
                             f"{scenario}-{generate_filename(current_config)}.csv")

                    # TODO: Decorator to measure time for all algorithms in calculate alignment
                    start_time = time.time()

                    alg = AlignmentAlgorithmFactory. \
                        get_alignment_algorithm(self._alignment_algorithm,
                                                **self.get_config_params(
                                                    pt_trace.to_dict('records'),
                                                    dt_trace.to_dict('records'),
                                                    current_config))

                    alignment_df = alg.calculate_alignment()

                    print(f"--- SCENARIO: {scenario} ---")
                    print(f"---{generate_filename(current_config)}"
                          f" : {(time.time() - start_time):.2f} seconds ---")

                    alignment_df.to_csv(alignment_filepath, index=False,
                                        encoding='utf-8', sep=',')

                    # if args.figures:
                    #     # --- GRAPHIC GENERATION ---
                    #     generate_alignment_graphic()

                    alignment_metrics = self._get_alignment_metrics(alignment_df, dt_trace,
                                                                    pt_trace,
                                                                    current_config,
                                                                    alg.score)
                    statistical_results_df = pd.concat(
                        [statistical_results_df,
                         pd.DataFrame.from_records([alignment_metrics])],
                        ignore_index=True)

                statistical_results_df.to_csv(os.path.join(self._output_results_directory,
                                                           global_results_filename), index=False)

    def _get_hyperparameters_combinations(self):
        return list(itertools.product(*self._get_hyperparameters_ranges()))

    def _get_alignment_metrics(self, alignment_df, pt_trace, dt_trace, input_dict, score):
        # --- DISTANCE ANALYSIS ---
        alignment_results = AnalysisFactory.create_instance \
            (self._alignment_algorithm, self._lca, alignment=alignment_df,
             dt_trace=dt_trace, pt_trace=pt_trace, system=self._system,
             selected_params=self._params, score=score, timestamp_label=self._timestamp_label)

        statistical_values = fu.get_property_values(alignment_results, self._methods)
        return {**fu.flatten_dictionary(input_dict),
                **fu.flatten_dictionary(statistical_values)}

    def _get_scenario(self, dt_file, pt_file):
        """
        Generate a unique filename by combining fileA and fileB in the format: <fileAfileB>
        and adding the param_interest

        :param dt_file: The filename for fileA.
        :param pt_file: The filename for fileB.
        :return: The combined unique filename.
        """
        return f"{os.path.splitext(dt_file)[0] + os.path.splitext(pt_file)[0]}" \
               f"-{self._param_interest.replace('/', '')}"

    def _get_hyperparameters_labels(self) -> list:
        return []

    def _get_hyperparameters_ranges(self) -> list:
        return []

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            PT_TRACE: pt_trace,
            DT_TRACE: dt_trace,
            SYSTEM: self._system,
            TIMESTAMP_LABEL: self._timestamp_label
        }
