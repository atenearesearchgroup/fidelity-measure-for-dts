import multiprocessing
import time
from ast import literal_eval

import pandas as pd
import pika

import window.alignment_config as ac
from algorithm import NeedlemanWunschAffineGap
from result_analysis import generate_alignment_graphic
from window.alignment_config import AlignmentConfiguration

TWIN_COMM = 'twin_comm'


class SlidingWindowProcessor:
    def __init__(self, window_size: int,
                 conf: AlignmentConfiguration,
                 manager: multiprocessing.Manager,
                 host: str = 'localhost',
                 timestep: int = 1,
                 expected_queues=None):
        """
        :param int window_size: The number of snapshots to process in each window alignment.
        :param AlignmentConfiguration conf: The alignment parameters configuration.
        :param int timestep: The number of newly received snapshots required to perform
        a new calculation.
        """
        self._dt_trace = []

        # i stands for integer type
        self._dt_count = 0

        self._pt_trace = []
        self._pt_count = 0

        self._processing_pointer = 0

        self.window_size = window_size
        self.timestep = timestep

        self._conf = conf
        self._host = host

        self._alignment_df = None
        self._alignment_fig = None

        if not expected_queues:
            self._routing = ['physical_twin', 'digital_twin']
        else:
            self._routing = expected_queues

    def consume_messages(self, routing_key):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        channel = connection.channel()

        channel.exchange_declare(exchange=TWIN_COMM, exchange_type='direct')

        result = channel.queue_declare(queue='')
        queue_name = result.method.queue

        for r in self._routing:
            channel.queue_bind(exchange=TWIN_COMM, queue=queue_name, routing_key=r)

        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"---- Received from {method.routing_key}: {message}")
            self.process_message(method.routing_key, message)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        print(f"Waiting for messages from {queue_name}. To exit, press CTRL+C")
        channel.start_consuming()

    def process_message(self, routing_key, message):
        # Store the message content in the corresponding list for further processing
        if routing_key == ac.DIGITAL_TWIN:
            self._dt_trace.append(literal_eval(message))
            self._dt_count += 1
        elif routing_key == ac.PHYSICAL_TWIN:
            self._pt_trace.append(literal_eval(message))
            self._pt_count += 1

        # If we have enough new elements to process a new window, we evaluate the alignment
        if len(self._pt_trace) - self._processing_pointer > self.window_size \
                and len(self._dt_trace) - self._processing_pointer > self.window_size \
                and self._pt_count >= self.timestep \
                and self._dt_count >= self.timestep:
            self.align()

    def align(self):
        # Take the slice from each trace to calculate the window alignment
        window_dt = self._dt_trace[self._processing_pointer:
                                   self._processing_pointer + self.window_size]
        window_pt = self._pt_trace[self._processing_pointer:
                                   self._processing_pointer + self.window_size]
        # Measure the time to process the alignment
        start_time = time.time()
        # Calculate the alignment
        print(f"--- SCENARIO: "
              f"[{self._processing_pointer}, "
              f"{self._processing_pointer + self.window_size}]---")
        ndw = NeedlemanWunschAffineGap(
            window_dt,
            window_pt,
            self._conf.system,
            initiate_gap=self._conf.init_gap,
            continue_gap=self._conf.cont_gap,
            low=self._conf.low,
            mad=self._conf.mad)
        self._alignment_df = ndw.calculate_alignment()
        # Alignment results
        print(f"--- Mad {self._conf.mad[self._conf.param_interest]:.2f}, "
              f"Init gap {self._conf.init_gap:.2f}, "
              f"Continue gap {self._conf.cont_gap:.2f}, "
              f"Low {self._conf.low} : "
              f"{(time.time() - start_time):.2f} seconds ---")
        # Print output alignment to .csv file
        output_dir_filename = self.__get_output_filename()
        self._alignment_df.to_csv(output_dir_filename, index=False, encoding='utf-8',
                                  sep=',')
        # --- GRAPHIC GENERATION ---
        self._alignment_fig = generate_alignment_graphic(self.alignment_df,
                                                         pd.DataFrame(window_dt),
                                                         pd.DataFrame(window_pt),
                                                         self._conf.params,
                                                         self._conf.timestamp_label,
                                                         output_path=output_dir_filename,
                                                         mad=self._conf.mad[
                                                             self._conf.param_interest],
                                                         open_gap=self._conf.init_gap,
                                                         continue_gap=self._conf.cont_gap,
                                                         engine=self._conf.engine)
        self._dt_count -= 1
        self._pt_count -= 1
        self._processing_pointer += 1

    def __get_output_filename(self):
        config_output_dir_filename = f"{self._conf.output_directory}sliding-window" \
                                     f"-({self._conf.init_gap:.2f}," \
                                     f"{self._conf.cont_gap:.2f})" \
                                     f"-{self._conf.low:.2f}" \
                                     f"-{self._conf.mad[self._conf.param_interest]:.2f}" \
                                     f"-{self._conf.param_interest.replace('/', '')}" \
                                     f"-[{self._processing_pointer}," \
                                     f"{self._processing_pointer + self.window_size}].csv"
        return config_output_dir_filename

    @property
    def alignment_df(self):
        return self._alignment_df

    @property
    def alignment_fig(self):
        return self._alignment_fig
