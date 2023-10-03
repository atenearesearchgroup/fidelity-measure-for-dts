import time

import pandas as pd
import pika


class TwinCSVDriver:
    def __init__(self, host: str, queue_name: str, csv_filename: str, timestamp_label: str):
        """
        :param str host: The address of the target server (e.g., 'localhost' or any IP).
        :param str queue_name: The name of the server's queue that will receive the information.
        :param str csv_filename: The name of the CSV file that includes the execution trace.
        :param str timestamp_label: The column name that includes the trace timestamp.
        """
        self._host = host
        self._queue_name = queue_name
        self._timestamp_label = timestamp_label
        self._data = pd.read_csv(csv_filename).to_dict('records')

    def send_data_to_server(self):

        # Open connection to the specified host
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))

        # Open a communication channel with the specified queue
        channel = connection.channel()
        channel.queue_declare(queue=self._queue_name)

        for index, item in enumerate(self._data):
            # Measure the timestep between snapshots
            if index <= 0:
                # First timestamp
                timestamp = float(self._data[index][self._timestamp_label])
            else:
                timestamp = float(self._data[index][self._timestamp_label]) \
                            - float(self._data[index - 1][self._timestamp_label])

            # Simulate sending data with the specified timestamp interval
            time.sleep(timestamp)

            # Send the data as a message to RabbitMQ
            message = str(self._data[index]).encode('utf-8')
            channel.basic_publish(exchange='', routing_key=self._queue_name, body=message)
            print(f"Sent: {self._queue_name} {message}")

        connection.close()
