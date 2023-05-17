import pandas as pd

from systems_config.system import SystemBase


class Lift(SystemBase):

    def is_low_complexity(self, snapshot=None):
        return abs(snapshot["accel(m/s2)"]) < 0.1 if isinstance(snapshot, pd.DataFrame) or snapshot else True
