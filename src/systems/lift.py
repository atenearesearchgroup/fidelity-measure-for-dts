from systems.system import SystemBase


class Lift(SystemBase):
    def is_low_complexity(self, key: str, value):
        return abs(value) < 0.1 if key == "accel(m/s2)" else False

    def filter_low_complexity(self, snapshot=None):
        return abs(snapshot["accel(m/s2)"]) < 0.1
