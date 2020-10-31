from typing import List, Any

from math import sqrt
from talipp.indicators.Indicator import Indicator
from talipp.indicators.WMA import WMA


class HMA(Indicator):
    """
    Hull Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period

        self.wma = WMA(period)
        self.wma2 = WMA(int(period / 2))
        self.hma = WMA(int(sqrt(period)))

        self.add_sub_indicator(self.wma)
        self.add_sub_indicator(self.wma2)
        self.add_managed_sequence(self.hma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.wma) < sqrt(self.period):
            return None

        self.hma.add_input_value(2.0 * self.wma2[-1] - self.wma[-1])

        if not self.hma.has_output_value():
            return None

        return self.hma[-1]