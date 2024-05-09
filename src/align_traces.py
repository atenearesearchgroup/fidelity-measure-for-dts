import argparse
import os

from batch.factory import BatchFactory


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures",
                        help="It processes the alignment and generates figures as image files",
                        default=True)
    parser.add_argument("--align_files",
                        help="Generate the .csv files with the resulting alignments",
                        default=True)
    parser.add_argument("--window-figures",
                        help="It provides an overview figure of all the windows.",
                        default=False)
    parser.add_argument("--engine",
                        help="Engine to process output pdf figures "
                             "(orca or kaleido). By default, kaleido.",
                        default='kaleido')
    parser.add_argument("--config", help="Config file name stored in the /src/config folder")
    return parser.parse_args()


def parse_arguments():
    args = build_parser()
    args.current_directory = os.path.join(os.getcwd(), "")
    return args


def execute_batch_config(args):
    batch_alignment = BatchFactory.get_batch_configuration(args)
    batch_alignment.execute_alignments()


def main():
    args = parse_arguments()

    # Set default values to test from IDE
    args.engine = 'kaleido'
    args.figures = False

    subfolder = 'variants_comparison'
    configs = [
        'lift_affine_variant.yaml',
        'lift_base_variant.yaml',
        'lift_lcaw_variant.yaml',
        'lift_lcaw_affine_variant.yaml'
    ]

    for config_file in configs:
        args.config = os.path.join(subfolder, config_file)
        execute_batch_config(args)


if __name__ == "__main__":
    main()
