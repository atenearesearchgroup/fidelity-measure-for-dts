"""
batch.alg_config
~~~~~~~~~~~~~~~~

An abstract class that generates alignment batches from a YAML file, using input ranges and
configuration parameters for sequence alignment algorithms.
"""
import itertools
import os
from abc import ABC, abstractmethod

import util.file as fu
from metrics.metrics_factory import AnalysisFactory
from systems import Lift, SystemBase
from systems.incubator import Incubator


class AlgorithmConfiguration(ABC):
    """
    This class generates alignment batches from a YAML file based on input ranges and configuration
    parameters for sequence alignment.

    Attributes:
        - current_directory (str): Path to the current working directory, to use relative paths
        - args (dict): input command-line arguments
    """

    PT_TRACE = 'pt_trace'
    DT_TRACE = 'dt_trace'
    SYSTEM = 'system'
    PARAM_INTEREST = 'param_interest'
    TIMESTAMP_LABEL = 'timestamp_label'

    def __init__(self, args, config):
        self.config = config
        self._parse_args(args)
        self._set_file_paths()
        self._initialize_analysis_labels()
        self._initialize_system()

    def _parse_args(self, args):
        self.current_directory = args.current_directory
        self.align_files = args.align_files
        self.window_figures = args.window_figures
        self.figures = args.figures
        self.engine = args.engine

    def _set_file_paths(self):
        """
        Access the YAML-parsed information and set the file paths for the input sequence files.
        """
        paths = self.config['paths']
        inputs = paths['input']

        # FILE PATHS
        input_directory = os.path.join(self.current_directory, inputs['main'])
        self.output_directory = os.path.join(self.current_directory, paths['output'])
        os.makedirs(self.output_directory, exist_ok=True)

        # DIGITAL TWIN
        self.dt_path = os.path.join(input_directory, inputs['dt'])
        self.dt_files = inputs['dt_files']

        # PHYSICAL TWIN
        self.pt_path = os.path.join(input_directory, inputs['pt'])
        self.pt_files = inputs['pt_files']

    def _initialize_analysis_labels(self):
        """
        Access the YAML-parsed information and set the properties of interest labels.
        """
        labels = self.config['labels']

        self.timestamp_label = labels.get('timestamp_label', 'timestamp(s)')
        self.param_interest = labels['param_interest']
        self.params = labels['params']
        self.group_by = labels.get('group_by', [])

    def _initialize_system(self):
        """
        Access the YAML-parsed information and initialize the set of methods for the output
        headers and the System object for the alignment.
        """
        system_name = self.config.get('system', 'System')
        systems = {
            'Lift': Lift,
            'Incubator': Incubator
        }
        if system_name in systems:
            self.system = systems[system_name]()
        else:
            self.system = SystemBase()

        self.lca = self.config.get('low_complexity_area', False)

        self.alignment_algorithm = self.config['alignment_alg']
        self.methods = fu.get_property_methods(AnalysisFactory.get_class
                                               (self.alignment_algorithm, self.lca))


    def get_hyperparameters_combinations(self):
        """
        It returns a list of tuples containing all possible combinations of parameter values
        based on user input ranges.
        """
        return list(itertools.product(*self.get_hyperparameters_ranges()))

    @abstractmethod
    def get_hyperparameters_labels(self) -> list:
        """
        :return: A list of the hyperparameter labels for the corresponding algorithm.
        """
        return []

    @abstractmethod
    def get_hyperparameters_ranges(self) -> list:
        """
        :return: A list of the hyperparameter ranges for the corresponding algorithm.
        """
        return []

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        """
        It generates a dictionary containing the necessary input parameters to instantiate the
        given algorithm. The dictionary serves as the creation attributes for the algorithm
        instance.

        :param pt_trace: The Physical Twin Trace
        :param dt_trace: The Digital Twin Trace
        :param current_config: The dictionary with the current configuration for the algorithm
        :return: A dictionary with the configuration parameters and their values.
        """
        return {
            self.PT_TRACE: pt_trace,
            self.DT_TRACE: dt_trace,
            **current_config
        }
