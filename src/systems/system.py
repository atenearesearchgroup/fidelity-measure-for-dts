from abc import ABC

import numpy as np
import pandas


class SystemBase(ABC):

    def snap_equals(self, dt_snapshot: np.array, pt_snapshot: np.array, keys: list, mad: np.array,
                    timestamp_label: str, low: float, include_timestamp: bool = False) -> float:
        result = 0.0
        for i, key in enumerate(keys):
            if include_timestamp or key != timestamp_label:
                dt_value = dt_snapshot[i]
                pt_value = pt_snapshot[i]

                if isinstance(dt_snapshot[i], (float, int)):
                    difference = abs(dt_value - pt_value)

                    dt_low = self.is_low_complexity(key, dt_value)
                    pt_low = self.is_low_complexity(key, pt_value)

                    if difference < mad[i]:
                        match_reward = (1 - difference / mad[i])
                        if dt_low and pt_low:  # Both low complexity region
                            result += match_reward / (low * 2)
                        elif dt_low or pt_low:  # At least one low complexity region
                            result += match_reward / low
                        else:
                            result += match_reward  # None in low complexity region
                    else:
                        result = 0
                        break
                else:
                    if dt_value == pt_value:
                        result += 1
                    else:
                        result = 0
                        break

        return result / (len(dt_snapshot) - (1 if not include_timestamp else 0))

    def distance(self, dt_snapshot: np.array, pt_snapshot: np.array, keys: list,
                 timestamp_label: str, include_timestamp: bool = False) -> float:
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
        return False

    def filter_low_complexity(self, df: pandas.DataFrame):
        return False
