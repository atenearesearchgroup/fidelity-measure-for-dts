from algorithm.system import SystemBase

class Incubator(SystemBase):

    def _is_low_complexity(self, snapshot: dict) -> bool:
        return False