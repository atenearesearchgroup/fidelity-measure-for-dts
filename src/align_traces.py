import argparse
import os

from batch_processing.config_factory import ConfigFactory

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures",
                        help="It processes the alignment and generates figures as image files",
                        action='store_true')
    parser.add_argument("--engine",
                        help="Engine to process output pdf figures "
                             "(orca or kaleido). By default, kaleido.",
                        default='kaleido')
    parser.add_argument("--config", help="Config file name stored in the /src/config folder")

    args = parser.parse_args()

    current_directory = os.path.join(os.getcwd(), "")
    alignment_config = ConfigFactory.get_batch_configuration(current_directory, args)
    alignment_config.execute_alignments()
