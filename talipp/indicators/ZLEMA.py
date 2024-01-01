from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.EMA import EMA
from talipp.indicators.Indicator import Indicator, InputModifierType


class ZLEMA(Indicator):
    """
    Zero Lag Exponential Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.lag = round((period - 1) / 2.0)

        self.ema = EMA(period)
        self.add_managed_sequence(self.ema)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.lag+1):
            return None

        self.ema.add(self.input_values[-1] + (self.input_values[-1] - self.input_values[-self.lag-1]))

        if not has_valid_values(self.ema):
            return None

        return self.ema[-1]
