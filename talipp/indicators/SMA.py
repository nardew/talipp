from typing import List, Any

from talipp.indicators.Indicator import Indicator


class SMA(Indicator):
    """
    Simple Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) > self.period:
            return self.output_values[-1] - \
                   (self.input_values[-self.period - 1] - self.input_values[-1]) / float(self.period)
        elif len(self.input_values) == self.period:
            return float(sum(self.input_values[-self.period:])) / self.period
        else: # len(self.input_values) < self.period
            return None