from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType


class EMA(Indicator):
    """
    Exponential Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None
        elif len(self.input_values) == self.period:
            return sum(self.input_values) / self.period
        else:
            mult = 2.0 / (self.period + 1.0)
            return float(mult * self.input_values[-1] + (1.0 - mult) * self.output_values[-1])