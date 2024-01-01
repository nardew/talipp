from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType


class WMA(Indicator):
    """
    Weighted Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.period = period

        self.denom_sum = period * (period + 1) / 2.0

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        s = 0.0
        for i in range(self.period, 0, -1):
            index = len(self.input_values) - self.period + i - 1  # decreases from end of array with increasing i
            s += self.input_values[index] * i

        return s / self.denom_sum
