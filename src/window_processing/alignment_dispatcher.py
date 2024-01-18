import datetime as dt
import multiprocessing
from ast import literal_eval

import pika

from batch_processing import AlignmentConfiguration
from window_processing.database_drivers.mongo import MongoManager
from window_processing.trace_consumer import TraceConsumer
from window_processing.window_align import WindowAlignments

TWIN_COMM = 'twin_comm'
PHYSICAL_TWIN = 'physical_twin'
DIGITAL_TWIN = 'digital_twin'


class SlidingWindowProcessor(TraceConsumer):
    def __init__(self, window_size: int,
                 conf: AlignmentConfiguration,
                 host: str = 'localhost',
                 expected_queues=None):
        """
        :param int window_size: The number of snapshots to process in each window alignment.
        :param AlignmentConfiguration conf: The alignment parameters configuration.
        :param int timestep: The number of newly received snapshots required to perform
        a new calculation.
        """
        super().__init__(host, expected_queues)
        self.window_size = window_size
        self._dt_trace, self._pt_trace = [], []
        self._processing_pointer = 0
        self._conf = conf

        self._window_alignment = WindowAlignments(conf)
        self._mongo_manager = MongoManager()
        self._alignment_id = None
        self._prefetch_count = self.window_size

    def consume_messages(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=self.window_size)
        channel.exchange_declare(exchange=TWIN_COMM, exchange_type='direct')
        queue_name = self.setup_queue(channel)

        alignment_dict = self.create_alignment_dict()
        self._alignment_id = MongoManager.insert_alignment_object(alignment_dict).inserted_id

        channel.basic_consume(queue=queue_name, on_message_callback=self._callback)
        print(f"Waiting for messages from {queue_name}. To exit, press CTRL+C")
        channel.start_consuming()

    def _callback(self, ch, method, properties, body):
        message = body.decode('utf-8')
        print(f"---- Received from {method.routing_key}: {message}")
        self.process_message(method.routing_key, message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def process_message(self, routing_key, message):
        if routing_key == DIGITAL_TWIN:
            self._dt_trace.append(literal_eval(message))
        elif routing_key == PHYSICAL_TWIN:
            self._pt_trace.append(literal_eval(message))

        if self.is_ready_to_align():
            self.align()

    def is_ready_to_align(self):
        return (
                len(self._pt_trace) >= self._processing_pointer + self.window_size
                and len(self._dt_trace) >= self._processing_pointer + self.window_size
        )

    def align(self):
        # Take the slice from each trace to calculate the window alignment
        window_dt = self.get_window(self._dt_trace)
        window_pt = self.get_window(self._pt_trace)

        align_process = multiprocessing.Process(target=self._store_alignment,
                                                args=(window_dt, window_pt,))
        align_process.start()
        # self._store_alignment(window_dt, window_pt)
        print('alignment started')

        self._processing_pointer += 1

    def get_window(self, trace):
        return trace[self._processing_pointer: self._processing_pointer + self.window_size]

    def _store_alignment(self, window_dt, window_pt):
        alignment_df, statistics_df = self._window_alignment.execute_alignments(window_dt,
                                                                                window_pt)
        MongoManager.insert_window_in_alignment(self._alignment_id, alignment_df)

    def create_alignment_dict(self):
        alignment_object = {
            'timestamp': dt.datetime.today(),
            'alg_name': self._conf.alignment_algorithm,
            'lca': self._conf.lca,
            'alg_hyperparams': {},
            'alignments': []
        }

        for index, hyperparam in enumerate(self._conf.get_hyperparameters_ranges()):
            # To process windows, we only take into account the "start" value
            # in the configuration file, that is why we use hyperparam[0]
            alignment_object['alg_hyperparams'][self._conf.get_hyperparameters_labels()[index]] = \
                float(hyperparam[0])

        return alignment_object

    def setup_queue(self, channel):
        result = channel.queue_declare(queue='', durable=True, exclusive=True)
        queue_name = result.method.queue

        for r in self._routing:
            channel.queue_bind(exchange=TWIN_COMM, queue=queue_name, routing_key=r)

        return queue_name
