import multiprocessing
import time

import pika

from algorithm import NeedlemanWunschAffineGap
from window.alignment_config import AlignmentConfiguration

DIGITAL_TWIN = 'digital_twin'
PHYSICAL_TWIN = 'physical_twin'


class SlidingWindowProcessor:
    def __init__(self, window_size: int,
                 conf: AlignmentConfiguration,
                 manager: multiprocessing.Manager,
                 host: str = 'localhost',
                 timestep: int = 1):
        """
        :param int window_size: The number of snapshots to process in each window alignment.
        :param AlignmentConfiguration conf: The alignment parameters configuration.
        :param int timestep: The number of newly received snapshots required to perform a new calculation.
        """
        self.dt_trace = manager.list()
        # i stands for integer type
        self.dt_count = multiprocessing.Value('i', 0)

        self.pt_trace = manager.list()
        self.pt_count = multiprocessing.Value('i', 0)

        self._processing_pointer = multiprocessing.Value('i', 0)

        self.window_size = window_size
        self.timestep = timestep

        self._conf = conf
        self._host = host

    def process_message(self, queue_name, message):
        if queue_name == DIGITAL_TWIN:
            self.dt_trace.append(eval(message))
            with self.dt_count.get_lock():
                self.dt_count.value += 1
        elif queue_name == PHYSICAL_TWIN:
            self.pt_trace.append(eval(message))
            with self.pt_count.get_lock():
                self.pt_count.value += 1

        if len(self.pt_trace) > self.window_size and len(self.dt_trace) > self.window_size and \
                self.pt_count.value >= self.timestep and self.dt_count.value >= self.timestep:
            start_time = time.time()
            print(self._processing_pointer.value)
            print(self._processing_pointer.value + self.window_size)
            ndw = NeedlemanWunschAffineGap(
                self.dt_trace[self._processing_pointer.value:self._processing_pointer.value + self.window_size],
                self.pt_trace[self._processing_pointer.value:self._processing_pointer.value + self.window_size],
                self._conf.system,
                initiate_gap=self._conf.init_gap,
                continue_gap=self._conf.continue_gap,
                low=self._conf.low,
                mad=self._conf.mad)
            alignment_df = ndw.calculate_alignment()

            print(
                f"--- SCENARIO: "
                f"[{self._processing_pointer.value}, {self._processing_pointer.value + self.window_size}]---")
            print(
                f"--- Mad {self._conf.mad[self._conf.param_interest]:.2f}, Init gap {self._conf.init_gap:.2f}, "
                f"Continue gap {self._conf.continue_gap:.2f}, Low {self._conf.low} : "
                f"{(time.time() - start_time):.2f} seconds ---")

            config_output_dir_filename = f"{self._conf.output_directory}sliding-window" \
                                         f"-({self._conf.init_gap:.2f}," \
                                         f"{self._conf.continue_gap:.2f})" \
                                         f"-{self._conf.low:.2f}" \
                                         f"-{self._conf.mad[self._conf.param_interest]:.2f}" \
                                         f"-{self._conf.param_interest.replace('/', '')}" \
                                         f"-[{self._processing_pointer.value},{self._processing_pointer.value + self.window_size}].csv"

            alignment_df.to_csv(config_output_dir_filename, index=False, encoding='utf-8', sep=',')

            with self.dt_count.get_lock():
                self.dt_count.value -= 1
            with self.pt_count.get_lock():
                self.pt_count.value -= 1
            with self._processing_pointer.get_lock():
                self._processing_pointer.value += 1

    def consume_messages(self, queue_name):
        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"---- Received from {queue_name}: {message}")
            self.process_message(queue_name, message)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(f"Waiting for messages from {queue_name}. To exit, press CTRL+C")
        channel.start_consuming()
