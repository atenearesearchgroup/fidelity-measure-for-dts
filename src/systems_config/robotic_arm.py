from systems_config.system import SystemBase


class RoboticArm(SystemBase):

    def snap_equals(self, dt_snapshot: dict, pt_snapshot: dict, tolerance: dict, timestamp_label: str, low: int = 5,
                    include_timestamp: bool = False) -> float:
        result = 0.0
        for key in dt_snapshot.keys():
            if include_timestamp or key != timestamp_label:
                dt_value = dt_snapshot[key]
                pt_value = pt_snapshot[key]

                dt_low = self._attribute_is_low_complexity(dt_value)
                pt_low = self._attribute_is_low_complexity(pt_value)

                if isinstance(dt_snapshot[key], float) or isinstance(dt_snapshot[key], int):
                    mad = tolerance[key]
                    difference = abs(dt_value - pt_value)

                    if difference < mad:
                        match_reward = (1 - difference / mad)
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
                    if dt_value[key] == pt_value[key]:
                        result += 1

        return result / (len(dt_snapshot) - 1)

    def _attribute_is_low_complexity(self, attribute):
        return abs(attribute) < 0.001
