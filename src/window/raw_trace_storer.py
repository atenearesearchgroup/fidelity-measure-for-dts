"""
window.raw_trace_storer
~~~~~~~~~~~~~~~~

The class that receives the Digital and Physical Twin traces via RabbitMQ queues and stores them
in InfluxDB
"""
import ast

from window.trace_consumer import TraceConsumer


class RawTraceStorer(TraceConsumer):
    """
    The class that receives the Digital and Physical Twin traces via RabbitMQ queues and stores them
    in InfluxDB
    """

    def process_message(self, routing_key, message):
        """
        When a message is received, this method executes the corresponding actions over it.
        :param routing_key: The routing key of the corresponding message
        :param message: The message body
        """
        prefix_mapping = {
            TraceConsumer.DIGITAL_TWIN: 'DT',
            TraceConsumer.PHYSICAL_TWIN: 'PT',
        }

        prefix = prefix_mapping.get(routing_key)
        if prefix is None:
            raise ValueError(f'[ERROR] Received unexpected routing key "{routing_key}"')

        message_content = ast.literal_eval(message)
        timestamp = message_content[self._timestamp_label]
        self._influx_manager.create_point(self._influx_bucket,
                                          f'{prefix}_Trace',
                                          message_content,
                                          timestamp)
