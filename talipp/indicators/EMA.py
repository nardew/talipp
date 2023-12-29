from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType


class EMA(Indicator):
    """
    Exponential Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None
        elif has_valid_values(self.input_values, self.period, exact=True):
            return sum(self.input_values[-self.period:]) / self.period
        else:
            mult = 2.0 / (self.period + 1.0)
            return float(mult * self.input_values[-1] + (1.0 - mult) * self.output_values[-1])
