from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.OBV import OBV
from talipp.ohlcv import OHLCV


class SOBV(Indicator):
    """
    Smoothed On Balance Volume

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.period = period

        self.obv = OBV()
        self.add_sub_indicator(self.obv)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.obv) < self.period:
            return None

        return sum(self.obv[-self.period:]) / float(self.period)
