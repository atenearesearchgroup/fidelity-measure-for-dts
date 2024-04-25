import faulthandler
import os

import yaml

from align_traces import parse_arguments, execute_batch_config
from batch.mode.window import WindowAlignmentMode as w
from batch.modifiers.delay import DelayWrapper as delay


def get_hyper_config(alter_type, len_anomaly):
    return {alter_type: len_anomaly,
            w.INTERVAL_PERIOD: {'start': int(len_anomaly / 5), 'step': int(len_anomaly / 5),
                                'end': len_anomaly + 1},
            w.INTERVAL_DURATION: {'start': int((len_anomaly * 2) / 5),
                                  'step': int((len_anomaly * 2) / 5),
                                  'end': len_anomaly * 2 + 1}}


def get_yaml_filepath(args, config_folder):
    return os.path.join(args.current_directory, config_folder, args.config)


def replace_params(hyperparameters, yaml_file):
    with open(yaml_file, 'r') as input_yaml:
        data = yaml.load(input_yaml, Loader=yaml.FullLoader)
        data['hyperparameters'].update(hyperparameters)
    return data


def write_yaml(data, yaml_file):
    with open(yaml_file, 'w') as output:
        output.write(yaml.dump(data, default_flow_style=False))
        output.flush()


def main():
    args = parse_arguments()

    # Set default values to test from IDE
    args.engine = 'kaleido'
    args.figures = False
    args.align_files = False

    config_folder = 'config_files'
    subfolder = 'window'
    configs = [
        'lift_affine_variant.yaml',
        # 'lift_base_variant.yaml',
        # 'lift_lcaw_variant.yaml',
        # 'lift_lcaw_affine_variant.yaml'
    ]

    len_anomalies = [10, 25, 50, 75, 100, 175, 250, 325, 400]
    for alter_type in [
        # an.LEN_ANOMALY,
        delay.LEN_DELAY]:
        for len_anomaly in len_anomalies:
            hyperparameters = get_hyper_config(alter_type, len_anomaly)

            for config_file in configs:
                args.config = os.path.join(subfolder, config_file)

                yaml_file = get_yaml_filepath(args, config_folder)
                data = replace_params(hyperparameters, yaml_file)
                write_yaml(data, yaml_file)

                print(f'## Starting executions with anomaly length {len_anomaly}')
                execute_batch_config(args)


if __name__ == "__main__":
    faulthandler.enable()
    main()
