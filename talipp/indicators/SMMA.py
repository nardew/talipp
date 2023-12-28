from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, ValueExtractorType


class SMMA(Indicator):
    """
    Smoothed Moving Average

    Output: a list of floats
    """
    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None
        elif has_valid_values(self.input_values, self.period, exact=True):
            return float(sum(self.input_values)) / self.period
        else:
            return (self.output_values[-1] * (self.period - 1) + self.input_values[-1]) / self.period
