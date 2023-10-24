import time

import pandas as pd
import pika

TWIN_COMM = 'twin_comm'

class TwinCSVDriver:
    def __init__(self, host: str, routing_key: str, csv_filename: str, timestamp_label: str):
        """
        :param str host: The address of the target server (e.g., 'localhost' or any IP).
        :param str routing_key: The name of the server's queue that will receive the information.
        :param str csv_filename: The name of the CSV file that includes the execution trace.
        :param str timestamp_label: The column name that includes the trace timestamp.
        """
        self._host = host
        self._routing_key = routing_key
        self._timestamp_label = timestamp_label
        self._data = pd.read_csv(csv_filename).to_dict('records')

    def send_data_to_server(self):
        # Open connection to the specified host
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))

        # Open a communication channel with the specified queue
        channel = connection.channel()

        # Create an exchange element to redirect messages with routing keys
        channel.exchange_declare(exchange=TWIN_COMM, exchange_type='direct')

        for index, item in enumerate(self._data):
            # Measure the timestep between snapshots
            if index <= 0:
                # First timestamp
                timestamp = float(self._data[index][self._timestamp_label])
            else:
                timestamp = float(self._data[index][self._timestamp_label]) \
                            - float(self._data[index - 1][self._timestamp_label])

            # Simulate sending data with the specified timestamp interval measured in seconds
            time.sleep(timestamp)

            # Send the data as a message to RabbitMQ
            message = str(self._data[index]).encode('utf-8')
            channel.basic_publish(exchange=TWIN_COMM, routing_key=self._routing_key, body=message)
            print(f"Sent: {self._routing_key} {message}")

        connection.close()
