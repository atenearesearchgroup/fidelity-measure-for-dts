from algorithm.case_study import CaseStudyBase

class IncubatorCaseStudy(CaseStudyBase):

    def _is_low_complexity(self, snapshot: dict) -> bool:
        return False