import multiprocessing
from ast import literal_eval

import pika

from batch_processing import AlignmentConfiguration
from window_processing.window_align import WindowAlignments

TWIN_COMM = 'twin_comm'
PHYSICAL_TWIN = 'physical_twin'
DIGITAL_TWIN = 'digital_twin'


class SlidingWindowProcessor:
    def __init__(self, window_size: int,
                 conf: AlignmentConfiguration,
                 host: str = 'localhost',
                 timestep: int = 0.1,
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

        if not expected_queues:
            self._routing = [PHYSICAL_TWIN, DIGITAL_TWIN]
        else:
            self._routing = expected_queues

        self._window_alignment = WindowAlignments(conf)

    def consume_messages(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        channel = connection.channel()
        # Each of the consumers may have only
        channel.basic_qos(prefetch_count=self.window_size)

        channel.exchange_declare(exchange=TWIN_COMM, exchange_type='direct')

        result = channel.queue_declare(queue='', durable=True, exclusive=True)
        queue_name = result.method.queue

        for r in self._routing:
            channel.queue_bind(exchange=TWIN_COMM, queue=queue_name, routing_key=r)

        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"---- Received from {method.routing_key}: {message}")
            self.process_message(method.routing_key, message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback, )

        print(f"Waiting for messages from {queue_name}. To exit, press CTRL+C")
        channel.start_consuming()

    def process_message(self, routing_key, message):
        # Store the message content in the corresponding list for further processing
        if routing_key == DIGITAL_TWIN:
            self._dt_trace.append(literal_eval(message))
            self._dt_count += 1
        elif routing_key == PHYSICAL_TWIN:
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

        align_process = multiprocessing.Process(target=self._window_alignment.execute_alignments,
                                                args=(window_dt, window_pt,))
        align_process.start()
        print('alignment started')

        self._dt_count -= 1
        self._pt_count -= 1
        self._processing_pointer += 1
