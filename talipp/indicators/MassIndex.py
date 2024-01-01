from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV


class MassIndex(Indicator):
    """
    Mass Index

    Output: a list of floats
    """

    def __init__(self, ema_period: int, ema_ema_period: int, ema_ratio_period: int, input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None, input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.EMA):
        super().__init__(input_modifier=input_modifier)

        self.ema_ratio_period = ema_ratio_period

        self.ma = MAFactory.get_ma(ma_type, ema_period)
        self.ma_ma = MAFactory.get_ma(ma_type, ema_ema_period)
        self.ma_ratio = []

        self.add_managed_sequence(self.ma)
        self.add_managed_sequence(self.ma_ma)
        self.add_managed_sequence(self.ma_ratio)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        self.ma.add(value.high - value.low)

        if not has_valid_values(self.ma, 1):
            return None

        self.ma_ma.add(self.ma[-1])

        if not has_valid_values(self.ma_ma, 1):
            return None

        self.ma_ratio.append(self.ma[-1] / float(self.ma_ma[-1]))

        if not has_valid_values(self.ma_ratio, self.ema_ratio_period):
            return None

        return sum(self.ma_ratio[-self.ema_ratio_period:])
