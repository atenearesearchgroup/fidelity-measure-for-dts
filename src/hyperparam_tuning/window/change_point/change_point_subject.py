from abc import ABC


class ChangePointSubject(ABC):
    def __init__(self, params, order_by, stat_filter):
        self._params = params
        self._order_by = order_by
        self._stat_filter = stat_filter

    @property
    def params(self):
        return self._params

    @property
    def order_by(self):
        return self._order_by

    @property
    def stat_filter(self):
        return self._stat_filter
