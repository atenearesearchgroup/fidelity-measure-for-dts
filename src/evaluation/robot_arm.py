from algorithm.system import SystemBase


class NiryoArm(SystemBase):

    def _is_low_complexity(self, snapshot: dict) -> bool:
        return False
