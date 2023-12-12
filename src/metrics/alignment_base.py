from abc import ABC
from typing import List

import pandas as pd

from systems.system import SystemBase
from util import clean_df


class AlignmentBase(ABC):
    PREFIX_DT = 'dt-'
    PREFIX_PT = 'pt-'

    def __init__(self, alignment: pd.DataFrame,
                 dt_trace: pd.DataFrame,
                 pt_trace: pd.DataFrame,
                 system: SystemBase,
                 selected_params: List[str],
                 score: float,
                 timestamp_label: str):
        # Traces to align
        self._dt_trace = clean_df(dt_trace)
        self._pt_trace = clean_df(pt_trace)
        # System information
        self._system = system
        # Alignment
        self._alignment = clean_df(alignment)
        # Relevant columns
        self._selected_params = selected_params
        self._timestamp_label = timestamp_label
        self._score = score
