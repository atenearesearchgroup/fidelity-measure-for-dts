from systems.system import SystemBase


class Incubator(SystemBase):
    def is_low_complexity(self, key: str, value):
        return 27 < abs(value) < 29 if key == "temperature(degrees)" else False

    def filter_low_complexity(self, snapshot=None):
        return 27 < abs(snapshot["temperature(degrees)"][0]) < 29
