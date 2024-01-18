import argparse
import os
from multiprocessing import Process

from batch_processing import ConfigFactory
from window_processing.alignment_dispatcher import SlidingWindowProcessor


def start_processor(conf):
    processor = SlidingWindowProcessor(5, conf)
    # Start separate threads for consuming messages from each producer
    thread1 = Process(target=processor.consume_messages)
    thread1.start()
    thread1.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--figures",
                        help="It processes the alignment and generates figures as image files",
                        action='store_true')
    parser.add_argument("--engine",
                        help="Engine to process output pdf figures (orca or kaleido). By default, kaleido.",
                        default='kaleido')
    parser.add_argument("--config", help="Config file name stored in the /src/config folder")

    # TODO: enter as parameter
    args = parser.parse_args()
    args.config = os.path.join('window', 'lift_affine_variant.yaml')

    curr_dir = os.path.join(os.getcwd(), "")
    alignment_config = ConfigFactory.get_batch_configuration(curr_dir, args)
    start_processor(alignment_config)
