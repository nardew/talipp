from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ma import MAFactory, MAType
from talipp.ohlcv import OHLCV


@dataclass
class StochVal:
    k: float = None
    d: float = None


class Stoch(Indicator):
    """
    Stochastic

    Output: a list of StochVal
    """

    def __init__(self, period: int, smoothing_period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None, ma_type: MAType = MAType.SMA):
        super().__init__(input_modifier=input_modifier, output_value_type=StochVal)

        self.period = period

        self.values_d = MAFactory.get_ma(ma_type, smoothing_period)
        self.add_managed_sequence(self.values_d)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        input_period = self.input_values[-1 * self.period:]

        highs = [value.high for value in input_period if value.high is not None]
        lows = [value.low for value in input_period if value.low is not None]

        max_high = max(highs)
        min_low = min(lows)

        if max_high == min_low:
            k = 100.0
        else:
            k = 100.0 * (self.input_values[-1].close - min_low) / (max_high - min_low)

        self.values_d.add(k)

        if has_valid_values(self.values_d, 1):
            d = self.values_d[-1]
        else:
            d = None

        return StochVal(k, d)
