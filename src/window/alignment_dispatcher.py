"""
window.alignment_dispatched
~~~~~~~~~~~~~~~~

The class that receives the Digital and Physical Twin traces via RabbitMQ queues.

Then, it waits until it had enough snapshots to fill a window.

When this condition is met, it creates a subprocess that performs the alignment of the traces
with the selected algorithm and then stores:
    (1) the raw alignment in MongoDB
    (2) the aggregated alignment statistics in InfluxDB

It repeats this process while it keeps receiving snapshots.
"""
import datetime as dt
import multiprocessing
from ast import literal_eval

from batch.config.alg_config import AlgorithmConfiguration
from window.align import WindowAlignments
from window.remote_drivers.mongo import MongoManager
from window.trace_consumer import TraceConsumer


class SlidingWindowProcessor(TraceConsumer):
    """
    The class that receives the Digital and Physical Twin traces via RabbitMQ queues.

    Then, it waits until it had enough snapshots to fill a window.

    When this condition is met, it creates a subprocess that performs the alignment of the traces
    with the selected algorithm and then stores:
        (1) the raw alignment in MongoDB
        (2) the aggregated alignment statistics in InfluxDB

    It repeats this process while it keeps receiving snapshots.
    """
    WINDOW_SIZE = 'window_size'
    TIMESTEP = 'timestep'

    def __init__(self,
                 alg_conf: AlgorithmConfiguration,
                 config_path: str,
                 expected_queues=None):
        super().__init__(config_path, expected_queues)

        self._dt_trace, self._pt_trace = [], []

        self._window_size = self._config[self.WINDOW_SIZE]
        self._timestep = self._config[self.TIMESTEP]

        self._conf = alg_conf
        self._window_alignment = WindowAlignments(alg_conf)

        self._alignment_id = None

    def _create_alignment_group(self):
        """
        It creates the parent structures in the databases to group the processed window alignments.

        In this case, it created an alignment object that will group the windows.
        """
        super()._create_alignment_group()
        alignment_dict = self.create_alignment_dict()
        self._alignment_id = MongoManager.insert_alignment_object(alignment_dict).inserted_id

    def process_message(self, routing_key, message):
        """
        When a message is received, this method executes the corresponding actions over it.

        Depending on the routing key, it separates the DT and PT snapshots in different lists to
        perform the alignments.
        :param routing_key: The routing key of the corresponding message
        :param message: The message body
        """
        if routing_key == TraceConsumer.DIGITAL_TWIN:
            self._dt_trace.append(literal_eval(message))
        elif routing_key == TraceConsumer.PHYSICAL_TWIN:
            self._pt_trace.append(literal_eval(message))

        if self._is_ready_to_align():
            self._align()

    def _is_ready_to_align(self):
        """
        :return: if the received unprocessed snapshots are at least the window size, we perform a
        window alignment.
        """
        return (
                len(self._pt_trace) >= self._window_size
                and len(self._dt_trace) >= self._window_size
        )

    def _align(self):
        """
        This method creates a subprocess that performs the alignment of the snapshots in the
        window and saves the results in the corresponding databases.
        """
        # Take the slice from each trace to calculate the window alignment
        window_dt = self.get_window(self._dt_trace)
        window_pt = self.get_window(self._pt_trace)

        align_process = multiprocessing.Process(target=self._store_alignment,
                                                args=(window_dt, window_pt,))
        align_process.start()
        self._store_alignment(window_dt, window_pt)
        print('alignment started')

        self._dt_trace = self._dt_trace[self._timestep:]
        self._pt_trace = self._pt_trace[self._timestep:]

    def get_window(self, trace):
        """
        It takes from a trace, the set of snapshots that will be processed as the next window.
        """
        return trace[: self._window_size]

    def _store_alignment(self, window_dt, window_pt):
        """
        Performs the alignment and stores the results in the corresponding databases.
        :param window_dt: Digital Twin snapshot window
        :param window_pt: Physical Twin snapshot window
        :return:
        """
        alignment_df, statistics_df = self._window_alignment.execute_alignments(window_dt,
                                                                                window_pt)
        MongoManager.insert_window_in_alignment(self._alignment_id, alignment_df)
        self._influx_manager.create_point(self._influx_bucket, 'Stats',
                                          statistics_df.to_dict('records')[0],
                                          window_pt[len(window_pt) - 1][self._timestamp_label])

    def create_alignment_dict(self):
        """
        :return: dictionary containing the object that will be stored in MongoDB
        """
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
