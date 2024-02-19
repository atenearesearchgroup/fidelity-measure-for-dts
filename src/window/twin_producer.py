"""
window.raw_trace_storer
~~~~~~~~~~~~~~~~

The class mimics the real-time behavior of the Physical and Digital Twins.

It reads a CSV file that contains the behavioral trace and simulates the production pace on the
real system based on the data.

The data is sent to the consumers via RabbitMQ.
"""
import time
from datetime import datetime, timezone, timedelta

import pandas as pd
import pika
import yaml

from window.trace_consumer import TraceConsumer


class TwinCSVDriver:
    """
    The class mimics the real-time behavior of the Physical and Digital Twins.

    It reads a CSV file that contains the behavioral trace and simulates the production pace on
    the real system based on the data.

    The data is sent to the consumers via RabbitMQ.
    """

    def __init__(self, config_path: str, routing_key: str, csv_filepath: str):
        """
        :param str config_path: The path of the configuration file.
        :param str routing_key: The name of the server's queue that will receive the information.
        :param str csv_filepath: The path of the CSV file that includes the execution trace.
        """
        with open(config_path, 'r', encoding='utf-8') as config_file:
            config = yaml.safe_load(config_file)

        self._host = config[TraceConsumer.RABBITMQ][TraceConsumer.HOST]
        self._timestamp_label = config[TraceConsumer.TIMESTAMP_LABEL]
        self._routing_key = routing_key
        self._data = pd.read_csv(csv_filepath).to_dict('records')

    def send_data_to_server(self):
        """
        This function reads from a CSV file a behavioral trace snapshot by snapshot and sends it
        through RabbitMQ.

        The snapshots are then delivered to the RabbitMQ exchange named 'twin_comm'.

        By keeping the sending pace of the trace, it simulates the actual behavior
        of the system in real-time.
        """
        # Open connection to the specified host
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))

        # Open a communication channel with the specified queue
        channel = connection.channel()

        # Create an exchange element to redirect messages with routing keys
        channel.exchange_declare(exchange=TraceConsumer.TWIN_COMM, exchange_type='direct')
        init_timestamp = datetime.now(timezone.utc)

        for index, item in enumerate(self._data):
            # Measure the timestep between snapshots
            if index <= 0:
                # First timestamp
                timestamp = float(self._data[index][self._timestamp_label])
            else:
                timestamp = float(self._data[index][self._timestamp_label]) \
                            - float(self._data[index - 1][self._timestamp_label])

            absolute_time = init_timestamp + timedelta(0, self._data[index][self._timestamp_label])
            message_data = self._data[index].copy()
            message_data[self._timestamp_label] = absolute_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            # Simulate sending data with the specified timestamp interval measured in seconds
            time.sleep(timestamp)

            # Send the data as a message to RabbitMQ
            message = str(message_data).encode('utf-8')
            channel.basic_publish(exchange=TraceConsumer.TWIN_COMM,
                                  routing_key=self._routing_key,
                                  body=message,
                                  properties=pika.BasicProperties(
                                      delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                  ))
            print(f"Sent: {self._routing_key} {message}")

        connection.close()
