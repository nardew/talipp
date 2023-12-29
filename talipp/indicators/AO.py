from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV


class AO(Indicator):
    """
    Awesome Oscillator

    Output: a list of floats
    """

    def __init__(self, fast_period: int, slow_period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None, ma_type: MAType = MAType.SMA):
        super().__init__(input_modifier=input_modifier)

        self.fast_period = fast_period
        self.slow_period = slow_period

        self.ma_fast = MAFactory.get_ma(ma_type, fast_period)
        self.ma_slow = MAFactory.get_ma(ma_type, slow_period)

        self.add_managed_sequence(self.ma_fast)
        self.add_managed_sequence(self.ma_slow)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        median = (self.input_values[-1].high + self.input_values[-1].low) / 2.0

        self.ma_fast.add(median)
        self.ma_slow.add(median)

        if not has_valid_values(self.ma_fast) or not has_valid_values(self.ma_slow):
            return None
        else:
            return self.ma_fast[-1] - self.ma_slow[-1]
