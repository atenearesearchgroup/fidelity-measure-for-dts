from algorithm.config.alg_config import AlgorithmConfiguration
from util.dict_util import get_range


class HyperparamsConfiguration(AlgorithmConfiguration):
    HYPERPARAMETERS = 'hyperparameters'

    def __init__(self, alg_config: AlgorithmConfiguration):
        self._alg_config = alg_config
        self._hyperparams = self._alg_config.config[self.HYPERPARAMETERS]

    def __getattr__(self, name):
        return getattr(self._alg_config, name)

    def get_alignment_metrics(self, alignment_df, pt_trace, dt_trace, input_parameters, score):
        return self._alg_config.get_alignment_metrics(alignment_df, pt_trace, dt_trace,
                                                      input_parameters, score)

    def get_scenario(self, dt_file, pt_file):
        return self._alg_config.get_scenario(dt_file, pt_file)

    def get_hyperparameters_labels(self) -> list:
        result = list(self._hyperparams.keys())
        result.extend(self._alg_config.get_hyperparameters_labels())
        return result

    def get_hyperparameters_ranges(self) -> list:
        result = [get_range(h) for h in self._hyperparams.values()]
        result.extend(self._alg_config.get_hyperparameters_ranges())
        return result

    def get_config_params(self, pt_trace, dt_trace, current_config=None):
        return self._alg_config.get_config_params(pt_trace, dt_trace, current_config)
