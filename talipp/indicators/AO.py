from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.SMA import SMA
from talipp.ohlcv import OHLCV


class AO(Indicator):
    """
    Awesome Oscillator

    Output: a list of floats
    """

    def __init__(self, period_fast: int, period_slow: int, input_values: List[OHLCV] = None):
        super(AO, self).__init__()

        self.periodFast = period_fast
        self.periodSlow = period_slow

        self.sma_fast = SMA(period_fast)
        self.sma_slow = SMA(period_slow)

        self.add_managed_sequence(self.sma_fast)
        self.add_managed_sequence(self.sma_slow)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        median = (self.input_values[-1].high + self.input_values[-1].low) / 2.0

        self.sma_fast.add_input_value(median)
        self.sma_slow.add_input_value(median)

        if not self.sma_fast.has_output_value() or not self.sma_slow.has_output_value():
            return None
        else:
            return self.sma_fast[-1] - self.sma_slow[-1]
