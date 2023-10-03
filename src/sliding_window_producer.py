import argparse
import multiprocessing
import os

from window.alignment_config import AlignmentConfiguration
from window.producer import TwinCSVDriver

DIGITAL_TWIN = 'digital_twin'
PHYSICAL_TWIN = 'physical_twin'


def start_producers(dt_path: str, pt_path: str, timestamp_label: str, host: str = 'localhost'):
    pt = TwinCSVDriver(host, PHYSICAL_TWIN, pt_path, timestamp_label)
    pt_thread = multiprocessing.Process(target=pt.send_data_to_server)
    # pt.send_data_to_server()

    dt = TwinCSVDriver(host, DIGITAL_TWIN, dt_path, timestamp_label)
    dt_thread = multiprocessing.Process(target=dt.send_data_to_server)
    # dt.send_data_to_server()

    pt_thread.start()
    dt_thread.start()

    pt_thread.join()
    dt_thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures", help="It processes the alignment and generates figures as image files",
                        action='store_true')
    parser.add_argument("--engine", help="Engine to process output pdf figures (orca or kaleido). By default, kaleido.",
                        default='kaleido')
    parser.add_argument("--config", help="Config file name stored in the /src/config folder")

    # TODO: enter as parameter
    args = parser.parse_args()
    args.figures = True
    args.engine = 'kaleido'
    args.config = '/lift_window.yaml'

    curr_dir = os.path.join(os.getcwd(), "")

    conf = AlignmentConfiguration(curr_dir, args)

    start_producers(conf.dt_path + conf.dt_file[0], conf.pt_path + conf.pt_files[0], conf.timestamp_label)
