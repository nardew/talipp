from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators import ATR
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ohlcv import OHLCV


@dataclass
class ChandeKrollStopVal:
    short_stop: float = None
    long_stop: float = None


class ChandeKrollStop(Indicator):
    """
    Chande Kroll Stop

    Output: a list of ChandeKrollStopVal objects
    """

    def __init__(self, atr_period: int, atr_mult: float, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier, output_value_type=ChandeKrollStopVal)

        self.atr_period = atr_period
        self.atr_mult = atr_mult
        self.period = period

        self.atr = ATR(atr_period)
        self.add_sub_indicator(self.atr)

        self.high_stop_list = []
        self.low_stop_list = []
        self.add_managed_sequence(self.high_stop_list)
        self.add_managed_sequence(self.low_stop_list)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.atr_period):
            return None

        if not has_valid_values(self.atr, 1):
            return None

        self.high_stop_list.append(max(self.input_values[-self.atr_period:], key = lambda x: x.high).high - self.atr[-1] * self.atr_mult)
        self.low_stop_list.append(min(self.input_values[-self.atr_period:], key = lambda x: x.low).low + self.atr[-1] * self.atr_mult)

        if not has_valid_values(self.high_stop_list, self.period):
            return None

        return ChandeKrollStopVal(max(self.high_stop_list[-self.period:]),
                                  min(self.low_stop_list[-self.period:]))
