from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.indicators.SMA import SMA
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

    def __init__(self, period: int, smoothing_period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.period = period

        self.values_d = SMA(smoothing_period)
        self.add_managed_sequence(self.values_d)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None

        input_period = self.input_values[-1 * self.period:]

        highs = [value.high for value in input_period]
        lows = [value.low for value in input_period]

        max_high = max(highs)
        min_low = min(lows)

        if max_high == min_low:
            k = 100.0
        else:
            k = 100.0 * (self.input_values[-1].close - min_low) / (max_high - min_low)

        self.values_d.add_input_value(k)

        if len(self.values_d) > 0:
            d = self.values_d[-1]
        else:
            d = None

        return StochVal(k, d)
