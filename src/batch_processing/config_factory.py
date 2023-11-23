import os

import plotly
import yaml

from batch_processing.alg_config.alignment_config import AlignmentConfiguration
from batch_processing.alg_config.dtw_lug_config import DynamicTimeWarpingLugaresiConfig
from batch_processing.alg_config.dtw_snaps_config import DynamicTimeWarpingSnapsConfig
from batch_processing.alg_config.lcss_events_config import LongestCommonSubsequenceEventsConfig
from batch_processing.alg_config.lcss_kpis_config import LongestCommonSubsequenceKPIsConfig
from batch_processing.alg_config.ndw_config import NeedlemanWunschConfiguration


class ConfigFactory:
    """
    A factory class for creating and managing configuration settings for each of the alignment
    algorithm variants.
    """

    @staticmethod
    def get_batch_configuration(current_directory, args) -> AlignmentConfiguration:
        config = ConfigFactory._load_configuration(current_directory, args)
        algorithms = {
            'NDW_Affine': NeedlemanWunschConfiguration,
            'NDW_Tolerance': NeedlemanWunschConfiguration,
            'DTW_Snaps': DynamicTimeWarpingSnapsConfig,
            'DTW_Lugaresi': DynamicTimeWarpingLugaresiConfig,
            'LCSS_KPIs': LongestCommonSubsequenceKPIsConfig,
            'LCSS_Events': LongestCommonSubsequenceEventsConfig
        }
        algorithm = config['alignment_alg']
        if algorithm in algorithms:
            return algorithms[algorithm](current_directory, args, config)
        raise ValueError(f"Invalid input algorithm name {algorithm}.")

    @staticmethod
    def _load_configuration(curr_dir: str, input_args):
        """
            Initialize the configuration parameters for the alignment and, if necessary, set
            the path to the Orca executable for processing the output alignments using Orca.

            :param curr_dir: Filepath to the algor
            :param input_args: An argparse.Namespace object containing command-line arguments.
        """
        if input_args.config[0] == '/':
            input_args = input_args[1:]

        config_file_path = os.path.join(curr_dir, 'config_files', input_args.config)
        try:
            with open(config_file_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)

            if input_args.figures and input_args.engine == "orca":
                plotly.io.orca.config.executable = config.get('orca_path', None)

        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Configuration file '{config_file_path}' not found.") from exc
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML format in the configuration file.") from exc

        return config
