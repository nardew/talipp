from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class VWMA(Indicator):
    """
    Volume Weighted Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.period = period

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None
        else:
            s = 0.0
            v = 0.0
            for value in self.input_values[-self.period:]:
                s += value.close * value.volume
                v += value.volume

            return s / v