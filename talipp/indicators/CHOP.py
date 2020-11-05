from math import log10
from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.ATR import ATR
from talipp.ohlcv import OHLCV


class CHOP(Indicator):
    """
    Choppiness Index

    Output: a list of OHLCV objects
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.period = period

        self.atr = ATR(1)
        self.add_sub_indicator(self.atr)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.atr) < self.period or len(self.input_values) < self.period:
            return None

        max_high = max(self.input_values[-self.period:], key = lambda x: x.high).high
        min_low = min(self.input_values[-self.period:], key = lambda x: x.low).low

        if max_high != min_low:
            return 100.0 * log10(sum(self.atr[-self.period:]) / (max_high - min_low) ) / log10(self.period)
        else:
            if len(self.output_values) > 0:
                return self.output_values[-1]
            else:
                return None