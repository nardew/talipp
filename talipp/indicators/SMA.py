from typing import List, Any

from talipp.indicators.Indicator import Indicator


class SMA(Indicator):
    """
    Simple Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None):
        super().__init__()

        self.period = period

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None
        else:
            return float(sum(self.input_values[len(self.input_values) - self.period:len(self.input_values)])) / self.period
