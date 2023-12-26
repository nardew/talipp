from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.SMA import SMA
from talipp.ohlcv import OHLCV


class AO(Indicator):
    """
    Awesome Oscillator

    Output: a list of floats
    """

    def __init__(self, fast_period: int, slow_period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super(AO, self).__init__()

        self.fast_period = fast_period
        self.slow_period = slow_period

        self.sma_fast = SMA(fast_period)
        self.sma_slow = SMA(slow_period)

        self.add_managed_sequence(self.sma_fast)
        self.add_managed_sequence(self.sma_slow)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        median = (self.input_values[-1].high + self.input_values[-1].low) / 2.0

        self.sma_fast.add_input_value(median)
        self.sma_slow.add_input_value(median)

        if not self.sma_fast.has_output_value() or not self.sma_slow.has_output_value():
            return None
        else:
            return self.sma_fast[-1] - self.sma_slow[-1]
