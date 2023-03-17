from algorithm.system import SystemBase

class Lift(SystemBase):

    def _is_low_complexity(self, snapshot: dict) -> bool:
        return abs(snapshot["accel(m/s2)"]) < 0.01