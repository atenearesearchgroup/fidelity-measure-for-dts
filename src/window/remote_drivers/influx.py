"""
window.remote_drivers.influx
~~~~~~~~~~~~~~~~

Class with auxiliary methods to store buckets and Points into InfluxDB.
"""
from influxdb_client import InfluxDBClient, Point

from util.float_util import parse_float


class InfluxManager:
    """
    Class with auxiliary methods to store buckets and Points into InfluxDB.

    Each of the methods creates its own client connection and closes it to enable the call
    from subprocesses.
    """

    def __init__(self, url: str, token: str, org: str):
        self._org = org
        self._url = url
        self._token = token

    def create_bucket(self, bucket_name: str):
        """
        Stores a bucket into InfluxDB
        :param bucket_name: name of the bucket
        """
        client = InfluxDBClient(url=self._url, token=self._token, org=self._org)
        if not client.buckets_api().find_bucket_by_name(bucket_name):
            client.buckets_api().create_bucket(bucket_name=bucket_name, org_id=self._org)
        client.close()

    def create_point(self, bucket: str, measurement: str, fields: dict, timestamp: str,
                     timestamp_label: str = 'timestamp(s)'):
        """
        Stores a Point into InfluxDB
        :param bucket: bucket in which the Point is stored
        :param measurement: measurement in which the Point it stores
        :param fields: dictionary of fields to store as Points
        :param timestamp: timestamp of the Point
        :param timestamp_label: key of the timestamp in the fields' dictionary
        :return:
        """
        client_api = InfluxDBClient(url=self._url, token=self._token, org=self._org).write_api()
        for key, value in fields.items():
            if key != timestamp_label:
                point = Point(measurement).field(key, parse_float(value)).time(timestamp)
                client_api.write(bucket=bucket, org=self._org, record=point)

        client_api.close()
