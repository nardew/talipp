from math import sqrt
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType


class StdDev(Indicator):
    """
    Standard Deviation

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        mean = sum(self.input_values[-self.period:]) / self.period
        return sqrt(sum([(item - mean)**2 for item in self.input_values[-self.period:]]) / self.period)
