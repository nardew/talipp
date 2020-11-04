from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class BOP(Indicator):
    """
    Balance Of Power

    Output: a list of floats
    """

    def __init__(self, input_values: List[OHLCV] = None):
        super().__init__()

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        return (value.close - value.open) / float(value.high - value.low)