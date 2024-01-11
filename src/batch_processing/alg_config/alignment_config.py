import itertools
import os

import util.file_util as fu
from metrics.metrics_factory import AnalysisFactory
from systems import Lift, SystemBase


class AlignmentConfiguration:
    """
    This class parses a YAML file to generate alignment batches based on specified input ranges
    and configuration parameters for a sequence alignment algorithm.

    Attributes:
        - current_directory (str): Path to the current working directory, to use relative paths
        - args (dict): input command-line arguments
    """

    PT_TRACE = 'pt_trace'
    DT_TRACE = 'dt_trace'

    def __init__(self, current_directory, args, config):
        self.current_directory = current_directory
        self.figures = args.figures
        self.engine = args.engine
        self.config = config
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
        paths = self.config['paths']
        inputs = paths['input']

        # FILE PATHS
        self._input_directory = os.path.join(self.current_directory, inputs['main'])
        self.output_directory = os.path.join(self.current_directory, paths['output'])

        # DIGITAL TWIN
        self.dt_path = os.path.join(self._input_directory, inputs['dt'])
        self.dt_file = inputs['dt_files']

        # PHYSICAL TWIN
        self.pt_path = os.path.join(self._input_directory, inputs['pt'])
        self.pt_files = inputs['pt_files']

    def _initialize_analysis_labels(self):
        """
        Access the YAML-parsed information and set the properties of interest labels.
        """
        labels = self.config['labels']

        self.timestamp_label = labels.get('timestamp_label', 'timestamp(s)')
        self._param_interest = labels['param_interest']
        self.params = labels['params']

    def _initialize_system(self):
        """
        Access the YAML-parsed information and initialize the set of methods for the output
        headers and the System object for the alignment.
        """
        system_name = self.config.get('system', 'System')
        self._system = Lift() if system_name == 'Lift' else SystemBase()

        self._lca = self.config.get('low_complexity_area', False)

        self.alignment_algorithm = self.config['alignment_alg']
        self._methods = fu.get_property_methods(AnalysisFactory.get_class
                                                (self.alignment_algorithm, self._lca))

    def _create_output_directories(self):
        """
            Create directories for storing individual result statistics and batch statistics.
        """
        self.output_results_directory = os.path.join(self.output_directory, 'results')
        directories = [self.output_directory, self.output_results_directory]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def get_hyperparameters_combinations(self):
        return list(itertools.product(*self._get_hyperparameters_ranges()))

    def get_alignment_metrics(self, alignment_df, pt_trace, dt_trace, input_dict, score):
        # --- DISTANCE ANALYSIS ---
        alignment_results = AnalysisFactory.create_instance \
            (self.alignment_algorithm, self._lca, alignment=alignment_df,
             dt_trace=dt_trace, pt_trace=pt_trace, system=self._system,
             selected_params=self.params, score=score, timestamp_label=self.timestamp_label)

        statistical_values = fu.get_property_values(alignment_results, self._methods)
        return {**fu.flatten_dictionary(input_dict),
                **fu.flatten_dictionary(statistical_values)}

    def get_scenario(self, dt_file, pt_file):
        """
        Generate a unique filename by combining fileA and fileB in the format: <fileAfileB>
        and adding the param_interest

        :param dt_file: The filename for fileA.
        :param pt_file: The filename for fileB.
        :return: The combined unique filename.
        """
        return f"{self.alignment_algorithm}-" \
               f"{'LCA_' if self._lca else ''}" \
               f"{os.path.splitext(dt_file)[0] + os.path.splitext(pt_file)[0]}" \
               f"-{self._param_interest.replace('/', '')}"

    def get_hyperparameters_labels(self) -> list:
        return []

    def _get_hyperparameters_ranges(self) -> list:
        return []

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return {
            self.PT_TRACE: pt_trace,
            self.DT_TRACE: dt_trace,
        }
