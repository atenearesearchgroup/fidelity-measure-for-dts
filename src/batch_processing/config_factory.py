import os

import plotly
import yaml

from batch_processing.alignment_config import AlignmentConfiguration
from batch_processing.needleman_wunsch_config import NeedlemanWunschConfiguration


class ConfigFactory:
    """
    A factory class for creating and managing configuration settings for each of the alignment
    algorithm variants.
    """

    @staticmethod
    def get_batch_configuration(current_directory, args) -> AlignmentConfiguration:
        config = ConfigFactory._load_configuration(current_directory, args)
        if 'NDW' in config['alignment_alg']:
            return NeedlemanWunschConfiguration(current_directory, config)
        raise ValueError(f"Invalid input algorithm name {config['alignment_alg']}.")

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
