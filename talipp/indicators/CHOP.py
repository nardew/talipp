from math import log10
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.ATR import ATR
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ohlcv import OHLCV


class CHOP(Indicator):
    """
    Choppiness Index

    Output: a list of OHLCV objects
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.period = period

        self.atr = ATR(1)
        self.add_sub_indicator(self.atr)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.atr, self.period) or not has_valid_values(self.input_values, self.period):
            return None

        max_high = max(self.input_values[-self.period:], key = lambda x: x.high).high
        min_low = min(self.input_values[-self.period:], key = lambda x: x.low).low

        if max_high != min_low:
            return 100.0 * log10(sum(self.atr[-self.period:]) / (max_high - min_low) ) / log10(self.period)
        else:
            return None
