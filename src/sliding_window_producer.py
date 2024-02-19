import argparse
import multiprocessing
import os

from batch.factory import ConfigFactory
from window.twin_producer import TwinCSVDriver

PHYSICAL_TWIN = 'physical_twin'
DIGITAL_TWIN = 'digital_twin'


def start_producer(curr_dir: str,
                   trace_path: str,
                   routing_key: str):
    config_path = os.path.join(curr_dir, 'window', 'remote_drivers', 'remote_config.yaml')
    twin = TwinCSVDriver(config_path, routing_key, trace_path)
    twin_process = multiprocessing.Process(target=twin.send_data_to_server)

    twin_process.start()
    return twin_process


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures",
                        help="It processes the alignment and generates figures as image files",
                        action='store_true')
    parser.add_argument("--engine",
                        help="Engine to process output pdf figures (orca or kaleido). By default, "
                             "kaleido.",
                        default='kaleido')
    parser.add_argument("--config", help="Config file name stored in the /src/config folder")

    args = parser.parse_args()
    args.config = os.path.join('window', 'nasa_mars.yaml')

    current_directory = os.path.join(os.getcwd(), "")
    alignment_config = ConfigFactory.get_batch_configuration(current_directory, args)

    pt_process = start_producer(current_directory,
                                alignment_config.pt_path + alignment_config.pt_files[0],
                                PHYSICAL_TWIN)

    dt_process = start_producer(current_directory,
                                alignment_config.dt_path + alignment_config.dt_file[0],
                                DIGITAL_TWIN)

    pt_process.join()
    dt_process.join()
