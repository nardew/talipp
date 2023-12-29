from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
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

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier, output_value_type=AroonVal)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period+1):
            return None

        # search in reversed list in order to get the right-most index
        days_high = self.period - max(reversed(range(self.period + 1)),
                                      key = lambda x: self.input_values[-self.period - 1:][x].high)
        days_low = self.period - min(reversed(range(self.period + 1)),
                                     key = lambda x: self.input_values[-self.period - 1:][x].low)

        return AroonVal(100.0 * (self.period - days_high) / self.period,
                        100.0 * (self.period - days_low) / self.period)
