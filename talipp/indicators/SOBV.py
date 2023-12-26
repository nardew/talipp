from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.OBV import OBV
from talipp.ohlcv import OHLCV


class SOBV(Indicator):
    """
    Smoothed On Balance Volume

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.obv = OBV()
        self.add_sub_indicator(self.obv)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.obv) < self.period:
            return None

        return sum(self.obv[-self.period:]) / float(self.period)
