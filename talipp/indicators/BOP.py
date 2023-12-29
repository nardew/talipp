from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.ohlcv import OHLCV


class BOP(Indicator):
    """
    Balance Of Power

    Output: a list of floats
    """

    def __init__(self, input_values: List[OHLCV] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        if value.high != value.low:
            return (value.close - value.open) / float(value.high - value.low)
        else:
            return None
