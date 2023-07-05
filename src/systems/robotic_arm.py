from systems_config.system import SystemBase


class RoboticArm(SystemBase):
    def is_low_complexity(self, key: str, value):
        return abs(value) < 0.001
