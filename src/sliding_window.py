import argparse
import os
from multiprocessing import Process

from batch.factory import ConfigFactory
from window.alignment_dispatcher import SlidingWindowProcessor
from window.raw_trace_storer import RawTraceStorer


def start_processor(config_path, alignment_config):
    alignment_dispatcher = SlidingWindowProcessor(alignment_config, config_path)
    raw_traces_processor = RawTraceStorer(config_path)
    # Start separate threads for consuming messages from each producer
    raw_traces_process = Process(target=raw_traces_processor.consume_messages)
    alignment_process = Process(target=alignment_dispatcher.consume_messages)
    raw_traces_process.start()
    alignment_process.start()
    raw_traces_process.join()
    alignment_process.join()


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
    args.config = os.path.join('window', 'nasa_mars.yaml')

    curr_dir = os.path.join(os.getcwd(), "")
    config_dir = os.path.join(curr_dir, 'window', 'remote_drivers', 'remote_config.yaml')
    alignment_config = ConfigFactory.get_batch_configuration(curr_dir, args)
    start_processor(config_dir, alignment_config)
