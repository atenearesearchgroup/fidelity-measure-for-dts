"""
window.trace_consumer
~~~~~~~~~~~~~~~~

Abstract class that includes the basic behavior for a RabbitMQ consumer with a temporal queue
that is fed by the exchange 'twin_comm'. It initializes a connection to InfluxDB and creates
a bucket.
"""
from abc import abstractmethod, ABCMeta

import pika
import yaml

from window.remote_drivers.influx import InfluxManager


class TraceConsumer(metaclass=ABCMeta):
    """
    Abstract class that includes the basic behavior for a RabbitMQ consumer with a temporal queue
    that is fed by the exchange 'twin_comm'.
    """
    TIMESTAMP_LABEL = 'timestamp_label'
    TWIN_COMM = 'twin_comm'
    PHYSICAL_TWIN = 'physical_twin'
    DIGITAL_TWIN = 'digital_twin'

    RABBITMQ = 'rabbitmq'
    INFLUXDB = 'influxdb'
    MONGODB = 'mongodb'

    HOST = 'host'
    PORT = 'port'

    def __init__(self,
                 config_path: str,
                 expected_queues=None):
        # config_file_path = os.path.join(curr_dir, 'window', 'remote_drivers', 'remote_config.yaml')

        with open(config_path, 'r', encoding='utf-8') as config_file:
            self._config = yaml.safe_load(config_file)

        self._timestamp_label = self._config[TraceConsumer.TIMESTAMP_LABEL]

        # RabbitMQ Initialization
        rabbit_config = self._config[self.RABBITMQ]
        self._rabbit_host = rabbit_config[self.HOST]
        self._rabbit_prefetch_count = rabbit_config['prefetch_count']
        self._routing = expected_queues or [self.PHYSICAL_TWIN, self.DIGITAL_TWIN]

        # InfluxDB Initialization
        influx_config = self._config[TraceConsumer.INFLUXDB]
        with open(influx_config['token_path']) as file:
            token = file.read().rstrip()

        self._influx_bucket = influx_config['bucket']
        self._influx_manager = InfluxManager(influx_config['url'],
                                             token,
                                             influx_config['org'])

    def consume_messages(self):
        """
        It establishes a remote connection with RabbitMQ, sets up basic structures in the
        corresponding databases, and begins to consume from the newly created RabbitMQ queue.
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._rabbit_host))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=self._rabbit_prefetch_count)
        channel.exchange_declare(exchange=self.TWIN_COMM, exchange_type='direct')
        queue_name = self.setup_queue(channel)

        self._create_alignment_group()

        channel.basic_consume(queue=queue_name, on_message_callback=self._callback)
        print(f"Waiting for messages from {queue_name}. To exit, press CTRL+C")
        channel.start_consuming()

    def _create_alignment_group(self):
        """
        It creates the parent structures in the databases to group the processed window alignments.

        In this case, it created the InfluxDB bucket to store the alignment statistics.
        """
        self._influx_manager.create_bucket(self._influx_bucket)

    def _callback(self, ch, method, properties, body):
        """
        This method is called whenever a message is received via RabbitMQ
        :param ch: pika.channel.Channel
        :param method: pika.spec.Basic.Return
        :param properties: pika.spec.BasicProperties
        :param body: bytes containing the message sent
        """
        message = body.decode('utf-8')
        print(f"---- Received from {method.routing_key}: {message}")
        self.process_message(method.routing_key, message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    @abstractmethod
    def process_message(self, routing_key, message):
        """
        When a message is received, this method executes the corresponding actions over it.
        :param routing_key: The routing key of the corresponding message
        :param message: The message body
        """
        raise NotImplementedError

    def setup_queue(self, channel) -> str:
        """
        It sets up a RabbitMQ temporal queue in the specified channel.
        :param channel: the pika.channel.Channel in which the queue is created
        :return: the name of the created queue
        """
        result = channel.queue_declare(queue='', durable=True, exclusive=True)
        queue_name = result.method.queue

        for r in self._routing:
            channel.queue_bind(exchange=self.TWIN_COMM, queue=queue_name, routing_key=r)

        return queue_name
