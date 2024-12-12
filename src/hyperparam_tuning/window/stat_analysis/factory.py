import re

from batch.modifiers.anomaly import AnomalyWrapper as an
from batch.modifiers.delay import DelayWrapper as de
from hyperparam_tuning.window.stat_analysis.anomaly import AnomalyStatAnalysis
from hyperparam_tuning.window.stat_analysis.delay import DelayStatAnalysis


class StatAnalysisFactory:
    def get_stat_analysis(self, path, filename):
        values = self._get_hyperparams_values(filename)
        modifier = self._get_position_key(self.modifiers, values)
        if modifier in self.modifiers:
            return self.modifiers[modifier](modifier, values, path, filename)
        raise ValueError(f'Invalid input modifier name {modifier}.')

    def _get_hyperparams_values(self, filename):
        parts = re.findall(r'([a-z]{2})_(-?\d+\.?\d*|\(\d+\.?\d*,\d+\.?\d*\))-?', filename)
        result = {}
        modifiers = self._get_modifiers()
        for p in parts:
            if p[0] in ['du', 'pe']:
                result[p[0]] = int(p[1])
            elif p[0] in modifiers:
                if re.match(r'\d+', p[1]):
                    result[f'{p[0]}_len'] = int(p[1])
                else:
                    result[f'{p[0]}_pos'] = [float(p) for p in re.findall(r'\d+\.?\d*', p[1])]

        return result

    def _get_modifiers(self):
        return [m[:2] for m in self.modifiers.keys()]

    def _get_position_key(self, modifiers, values):
        for modifier in modifiers:
            if f'{modifier[:2]}_pos' in values:
                return modifier
        return ''

    @property
    def modifiers(self):
        return {
            de.DELAY: DelayStatAnalysis,
            an.ANOMALY: AnomalyStatAnalysis
        }
