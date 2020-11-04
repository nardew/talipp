from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.indicators.SMA import SMA
from talipp.ohlcv import OHLCV


@dataclass
class AroonVal:
    up: float = None
    down: float = None


class Aroon(Indicator):
    """
    Aroon Up/Down

    Output: a list of AroonVal
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.period = period

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period + 1:
            return None

        # search in reversed list in order to get the right-most index
        days_high = self.period - max(reversed(range(self.period + 1)),
                                      key = lambda x: self.input_values[-self.period - 1:][x].high)
        days_low = self.period - min(reversed(range(self.period + 1)),
                                     key = lambda x: self.input_values[-self.period - 1:][x].low)

        return AroonVal(100.0 * (self.period - days_high) / self.period,
                        100.0 * (self.period - days_low) / self.period)