from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.OBV import OBV
from talipp.ohlcv import OHLCV


class SOBV(Indicator):
    """
    Smoothed On Balance Volume

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.period = period

        self.obv = OBV()
        self.add_sub_indicator(self.obv)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.obv, self.period):
            return None

        return sum(self.obv[-self.period:]) / float(self.period)
