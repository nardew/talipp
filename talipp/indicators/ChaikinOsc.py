from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.AccuDist import AccuDist
from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV


class ChaikinOsc(Indicator):
    """
    Chaikin Oscillator

    Output: a list of floats
    """

    def __init__(self, fast_period: int, slow_period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None,
                 value_extractor: ValueExtractorType = None, ma_type: MAType = MAType.EMA):
        super().__init__(value_extractor = value_extractor)

        self.fast_period = fast_period
        self.slow_period = slow_period

        self.accu_dist = AccuDist()
        self.add_sub_indicator(self.accu_dist)

        self.ma_fast = MAFactory.get_ma(ma_type, fast_period, value_extractor=value_extractor)
        self.add_managed_sequence(self.ma_fast)

        self.ma_slow = MAFactory.get_ma(ma_type, slow_period, value_extractor=value_extractor)
        self.add_managed_sequence(self.ma_slow)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.accu_dist):
            return None

        self.ma_fast.add_input_value(self.accu_dist[-1])
        self.ma_slow.add_input_value(self.accu_dist[-1])

        if not has_valid_values(self.ma_fast) or not has_valid_values(self.ma_slow):
            return None

        return self.ma_fast[-1] - self.ma_slow[-1]
