from abc import ABC

import numpy as np
import pandas
from numba import jit


class SystemBase(ABC):

    def snap_equals(self, dt_snapshot, pt_snapshot, mad,
                    types, timestamp_range, dt_low, pt_low, low,
                    include_timestamp: bool = False) -> float:
        """
        Calculate the similarity score between two snapshots based on matching timestamps.

        This function calculates the similarity score between two snapshots of timeseries data.
        It iterates over a range of timestamps and checks if the corresponding values in the
        `dt_snapshot` and `pt_snapshot` match. The similarity score is then computed based
        on differences between values.

        :param timestamp_range: The indices of the attributes to consider.
        :type timestamp_range: range
        :param dt_snapshot: The digital twin snapshot.
        :type dt_snapshot: numpy.ndarray
        :param pt_snapshot: The physical twin snapshot.
        :type pt_snapshot: numpy.ndarray
        :param types: A bool array indicating whether timestamps are included or not in the comparison.
        :type types: numpy.ndarray
        :param mad: The maximum acceptable distance allowed for matching attributes.
        :type mad: numpy.ndarray
        :param low: A weighting factor to reduce the influence of low-complexity areas.
        :type low: float
        :param dt_low: A binary array indicating lca in the digital twin trace.
        :type dt_low: numpy.ndarray
        :param pt_low: A binary array indicating lca in the physical twin trace.
        :type pt_low: numpy.ndarray
        :param include_timestamp: Flag indicating whether to include timestamp in the calculation.
        :type include_timestamp: bool
        :return: The similarity score between the two snapshots.
        :rtype: float
        :raises ValueError: If input snapshots are not of compatible lengths or types.
        """
        return _snap_equals(timestamp_range, dt_snapshot, pt_snapshot, types, mad, low, dt_low,
                            pt_low, include_timestamp)

    def distance(self, dt_snapshot: np.array, pt_snapshot: np.array, keys: list,
                 timestamp_label: str, include_timestamp: bool = False) -> float:
        """
        Calculate the distance between two snapshots based on specified keys.

        This method calculates the distance between two snapshots `dt_snapshot`
        and `pt_snapshot` based on specified keys. The distance is computed
        by comparing corresponding values of the specified keys. If `include_timestamp` is set
        to True, the timestamp values will be included in the comparison, otherwise, they are
        excluded.

        :param dt_snapshot: The digital twin snapshot
        :type dt_snapshot: numpy.ndarray
        :param pt_snapshot: The physical twin snapshot
        :type pt_snapshot: numpy.ndarray
        :param keys: The keys to consider for comparison.
        :type keys: list
        :param timestamp_label: The label indicating the timestamp in the snapshots.
        :type timestamp_label: str
        :param include_timestamp: Flag indicating whether to include timestamp in the comparison.
                                  Defaults to False.
        :type include_timestamp: bool, optional
        :return: The distance between the two snapshots based on specified keys.
        :rtype: float
        """
        result = 0.0
        for i, key in enumerate(keys):
            if include_timestamp or key != timestamp_label:
                dt_value = dt_snapshot[i]
                pt_value = pt_snapshot[i]

                if isinstance(dt_snapshot[i], (float, int)):
                    result += abs(dt_value - pt_value)
                else:
                    if dt_value[i] == pt_value[i]:
                        result += 1

        return result / (len(dt_snapshot) - (1 if not include_timestamp else 0))

    def is_low_complexity(self, key: str, value):
        """
        Check if the given key-value pair belongs to a low-complexity area.

        :param key: The key of the attribute.
        :type key: str
        :param value: The corresponding value.
        :return: True if the key-value pair belongs to a lca, otherwise False.
        :rtype: bool
        """
        return False

    def filter_low_complexity(self, df: pandas.DataFrame):
        """
        Returns the low-complexity area snapshots from the given DataFrame.

        :param df: The DataFrame to filter.
        :type df: pandas.DataFrame
        :return: The filtered dataframe. Otherwise, False, indicating that no filtering is done.
        :rtype: bool
        """
        return df.apply(lambda x: False, axis=1)


@jit(nopython=True)
def _snap_equals(timestamp_range, dt_snapshot, pt_snapshot, types, mad, low, dt_low, pt_low,
                 include_timestamp):
    """
    Calculate the similarity score between two snapshots based on matching timestamps.
    """
    result = 0.0
    for i in timestamp_range:
        dt_value = dt_snapshot[i]
        pt_value = pt_snapshot[i]

        if types[i]:
            difference = abs(dt_value - pt_value)
            m = mad[i]
            if difference < m:
                match_weight = (low * (int(dt_low[i]) + int(pt_low[i])))

                match_reward = (1 - difference / m)
                result += match_reward / match_weight if match_weight > 0 else match_reward
            else:
                return 0
        else:
            if dt_value == pt_value:
                result += 1
            else:
                return 0

    return result / (len(dt_snapshot) - (1 if not include_timestamp else 0))
