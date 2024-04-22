"""
batch.factory
~~~~~~~~~~~~~~~~

A factory class for creating and managing configuration settings for each of the alignment
algorithm variants.
"""
import os

import plotly
import yaml

from algorithm.config.alg_config import AlgorithmConfiguration
from algorithm.config.dtw.dtw_lug import DynamicTimeWarpingLugaresiConfig
from algorithm.config.dtw.dtw_snaps import DynamicTimeWarpingSnapsConfig
from algorithm.config.lcss.lcss_events import LongestCommonSubsequenceEventsConfig
from algorithm.config.lcss.lcss_kpis import LongestCommonSubsequenceKPIsConfig
from algorithm.config.ndw.ndw import NeedlemanWunschConfiguration
from algorithm.config.wrapper.hyperparams import HyperparamsConfiguration


class ConfigFactory:
    """
    A factory class for creating and managing configuration settings for each of the alignment
    algorithm variants.
    """

    @staticmethod
    def get_algorithm_configuration(args) -> AlgorithmConfiguration:
        """
        Factory method that returns an instance of the corresponding AlgorithmConfiguration
        subclass to perform an alignment.
        and export results.
        :param args: The argparse object with the user input.
        :return: The corresponding AlgorithmConfiguration instance
        """
        algorithms = {
            'NDW_Affine': NeedlemanWunschConfiguration,
            'NDW_Tolerance': NeedlemanWunschConfiguration,
            'DTW_Snaps': DynamicTimeWarpingSnapsConfig,
            'DTW_Lugaresi': DynamicTimeWarpingLugaresiConfig,
            'LCSS_KPIs': LongestCommonSubsequenceKPIsConfig,
            'LCSS_Events': LongestCommonSubsequenceEventsConfig
        }
        config = ConfigFactory._load_configuration(args)
        algorithm = config.get('alignment_alg')
        if algorithm and algorithm in algorithms:
            alg_config = algorithms[algorithm](args, config)
            if HyperparamsConfiguration.HYPERPARAMETERS in config:
                alg_config = HyperparamsConfiguration(alg_config)
            return alg_config
        raise ValueError(f"Invalid input algorithm name {algorithm}.")

    @staticmethod
    def _load_configuration(args):
        """
        Initialize the configuration parameters for the alignment and, if necessary, set
        the path to the Orca executable for processing the output alignments using Orca.

        :param args: An argparse.Namespace object containing command-line arguments.
        """
        args = ConfigFactory._remove_initial_path_bar(args)
        try:
            config_file_path = os.path.join(args.current_directory, 'config_files', args.config)
            with open(config_file_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)

            ConfigFactory._set_orca_executable_path(args, config)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Configuration file '{config_file_path}' not found.") from exc
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML format in the configuration file.") from exc

        return config

    @staticmethod
    def _set_orca_executable_path(args, config):
        if args.figures and args.engine == "orca":
            plotly.io.orca.config.executable = config.get('orca_path', None)

    @staticmethod
    def _remove_initial_path_bar(args):
        if args.config[0] == '/':
            args.config = args.config[1:]
        return args
