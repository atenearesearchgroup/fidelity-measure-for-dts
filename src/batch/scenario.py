import os

import pandas as pd

from batch.execution import Execution


class Scenario():
    def __init__(self, alg_config, pt_file, dt_file):
        self.folder = None
        self.alg_config = alg_config

        self._dt_file = dt_file
        self._pt_file = pt_file
        self._dt_trace = self._filter_csv(os.path.join(alg_config.dt_path, dt_file))
        self._pt_trace = self._filter_csv(os.path.join(alg_config.pt_path, pt_file))

    @property
    def dt_trace(self):
        return self._dt_trace

    @property
    def pt_trace(self):
        return self._pt_trace

    def get_name(self, extension=''):
        """
        Generate a unique filename by combining fileA and fileB in the format: <fileAfileB>
        and adding the param_interest

        :param dt_file: The filename for fileA.
        :param pt_file: The filename for fileB.
        :return: The combined unique filename.
        """
        return f"{self.alg_config.alignment_algorithm}-" \
               f"{'LCA_' if self.alg_config.lca else ''}" \
               f"{os.path.splitext(self._dt_file)[0]}" \
               f"{os.path.splitext(self._pt_file)[0]}" \
               f"-{self.alg_config.param_interest.replace('/', '')}" \
               f"{extension}"

    def _filter_csv(self, filepath):
        return pd.read_csv(filepath) \
            .filter(items=[self.alg_config.timestamp_label, *self.alg_config.params])

    def create_folder(self):
        self.folder = os.path.join(self.alg_config.output_directory,
                                   self.get_name())
        os.makedirs(self.folder, exist_ok=True)

    def create_execution(self, current_config_tuple):
        return Execution(self, current_config_tuple)
