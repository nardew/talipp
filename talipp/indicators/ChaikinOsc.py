from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.EMA import EMA
from talipp.indicators.AccuDist import AccuDist
from talipp.ohlcv import OHLCV


class ChaikinOsc(Indicator):
    """
    Chaikin Oscillator

    Output: a list of floats
    """

    def __init__(self, fast_period: int, slow_period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.fast_period = fast_period
        self.slow_period = slow_period

        self.accu_dist = AccuDist()
        self.add_sub_indicator(self.accu_dist)

        self.ema_fast = EMA(fast_period)
        self.add_managed_sequence(self.ema_fast)

        self.ema_slow = EMA(slow_period)
        self.add_managed_sequence(self.ema_slow)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not self.accu_dist.has_output_value():
            return None

        self.ema_fast.add_input_value(self.accu_dist[-1])
        self.ema_slow.add_input_value(self.accu_dist[-1])

        if not self.ema_fast.has_output_value() or not self.ema_slow.has_output_value():
            return None

        return self.ema_fast[-1] - self.ema_slow[-1]
