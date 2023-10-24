import argparse
import multiprocessing
import os

import window.alignment_config as ac
from window.alignment_config import AlignmentConfiguration
from window.dashboard import AlignmentDashboard


def start_processor(conf):
    with multiprocessing.Manager() as manager:
        processor = AlignmentDashboard(5, conf, manager)

        # Start separate threads for consuming messages from each producer
        thread1 = multiprocessing.Process(target=processor.consume_messages,
                                          args=(ac.PHYSICAL_TWIN,))
        thread1.start()
        thread1.join()


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

    start_processor(conf)
