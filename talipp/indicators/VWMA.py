from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.ohlcv import OHLCV


class VWMA(Indicator):
    """
    Volume Weighted Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None
        else:
            s = 0.0
            v = 0.0
            for value in self.input_values[-self.period:]:
                s += value.close * value.volume
                v += value.volume

            return s / v
