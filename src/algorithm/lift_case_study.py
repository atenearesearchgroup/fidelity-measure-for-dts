from algorithm.case_study import CaseStudyBase

class LiftCaseStudy(CaseStudyBase):

    def _is_low_complexity(self, snapshot: dict) -> bool:
        return abs(snapshot["accel(m/s2)"]) < 0.01