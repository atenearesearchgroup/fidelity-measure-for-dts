import plotly
import yaml

import util.file_util as fu
from metrics.alignment import Alignment
from metrics.alignment_lca import AlignmentLCA
from systems import Lift, SystemBase

MAD = 'mad'
LOW = 'low'
INIT_GAP = 'init_gap'
CONT_GAP = 'cont_gap'


class AlignmentConfiguration:
    def __init__(self, current_directory, args):
        self._current_directory = current_directory

        # Read the YAML file
        with open(current_directory + '/config_files/' + args.config, 'r') as file:
            config = yaml.safe_load(file)

        # ORCA EXECUTABLE PATH
        if args.figures and args.engine == "orca":
            plotly.io.orca.config.executable = config['orca_path']

        # FILE PATHS
        self._input_directory = current_directory + config['paths']['input']['main']
        self._output_directory = current_directory + config['paths']['output']

        # DIGITAL TWIN
        self._dt_path = self._input_directory + config['paths']['input']['dt']
        self._dt_file = config['paths']['input']['dt_files']

        # PHYSICAL TWIN
        self._pt_path = self._input_directory + config['paths']['input']['pt']
        self._pt_files = config['paths']['input']['pt_files']

        # ANALYSIS PARAMETERS
        self._timestamp_label = config['labels']['timestamp_label']
        self._param_interest = config['labels']['param_interest']
        self._params = config['labels']['params']

        # INPUT PARAMETERS
        ranges = config['ranges']

        # Calculate Maximum Acceptable Distance (MAD)
        self._max_acceptable_dist = ranges['mad']['start']

        # Calculate Weight for Low complexity areas
        self._low = ranges['low']['start']

        # Calculate Weights for Affine Gap
        self._init_gap = ranges['init_gap']['start']

        self._continue_gap = ranges['cont_gap']['start']

        if config['system'] == 'Lift':
            self._system = Lift()
            self._methods = fu.get_property_methods(AlignmentLCA)
        else:
            self._system = SystemBase()
            self._methods = fu.get_property_methods(Alignment)

    @property
    def output_directory(self):
        return self._output_directory

    @property
    def pt_files(self):
        return self._pt_files

    @property
    def pt_path(self):
        return self._pt_path

    @property
    def dt_file(self):
        return self._dt_file

    @property
    def dt_path(self):
        return self._dt_path

    @property
    def param_interest(self):
        return self._param_interest

    @property
    def timestamp_label(self):
        return self._timestamp_label

    @property
    def params(self):
        return self._params

    @property
    def system(self):
        return self._system

    @property
    def methods(self):
        return self._methods

    @property
    def low(self):
        return self._low

    @property
    def mad(self):
        formed_mad = {self._timestamp_label: self._max_acceptable_dist}
        formed_mad.update({p: self._max_acceptable_dist for p in self._params})
        return formed_mad

    @property
    def init_gap(self):
        return self._init_gap

    @property
    def continue_gap(self):
        return self._continue_gap
