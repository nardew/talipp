from typing import List, Any
from math import sqrt

from talipp.indicators.Indicator import Indicator, ValueExtractorType


class StdDev(Indicator):
    """
    Standard Deviation

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None
        else:
            mean = sum(self.input_values[-self.period:]) / self.period
            return sqrt(sum([(item - mean)**2 for item in self.input_values[-self.period:]]) / self.period)