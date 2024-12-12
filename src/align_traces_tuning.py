import faulthandler
import os

import yaml

from align_traces import parse_arguments, execute_batch_config
from batch.mode.window import WindowAlignmentMode as w


def get_hyper_config(alter_type, len_anomaly, duration, period, position=None):
    result = {
        f'{alter_type}_len': len_anomaly,
        w.INTERVAL_DURATION: duration,
        w.INTERVAL_PERIOD: period,
    }
    if position is not None:
        result[f'{alter_type}_pos'] = position
    return result


def get_yaml_filepath(args, config_folder):
    return os.path.join(args.current_directory, config_folder, args.config)


def replace_params(hyperparameters, yaml_file):
    with open(yaml_file, 'r') as input_yaml:
        data = yaml.load(input_yaml, Loader=yaml.FullLoader)
        data['hyperparameters'] = hyperparameters
    return data


def write_yaml(data, yaml_file):
    with open(yaml_file, 'w') as output:
        output.write(yaml.dump(data, default_flow_style=False))
        output.flush()


def main():
    args = parse_arguments()

    # Set default values to test from IDE
    args.engine = 'kaleido'
    args.figures = True
    args.align_files = True
    args.window_figures = True

    config_folder = 'config_files'
    subfolder = 'window'
    configs = [
        'lift_affine_variant.yaml',
        # 'incubator_comparison.yaml',
        # 'incubator_base.yaml'
    ]

    len_anomalies = [
        # 10,
        # 10,
        # 25,
        # 75, 100
        # , 150, 250, 325, 400
    ]
    len_durs = [
        # 5, *range(10, 150, 10)
    ]
    # range(2, 28, 2)
    len_pers = len_durs
    # range(2, 6, 2)
    # for i in range(5):
    # for alter_type in [
    #     # an.ANOMALY,
    #     #de.DELAY
    # ]:
    #     for len_anomaly in len_anomalies:
    #         for len_per in len_pers:
    #             for len_dur in len_durs:
    #

    hyperparameters = {}
    for config_file in configs:
        args.config = os.path.join(subfolder, config_file)

        yaml_file = get_yaml_filepath(args, config_folder)
        # data = replace_params(hyperparameters, yaml_file)
        # write_yaml(data, yaml_file)
        execute_batch_config(args)


if __name__ == "__main__":
    faulthandler.enable()
    main()
