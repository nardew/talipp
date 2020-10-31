from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.indicators.RSI import RSI
from talipp.indicators.SMA import SMA


@dataclass
class StochRSIVal:
    k: float = None
    d: float = None


class StochRSI(Indicator):
    """
    Stochastic RSI

    Output: a list of StochRSIVal
    """

    def __init__(self, rsi_period: int, stoch_period: int, smoothing_period_k: int, smoothing_period_d: int, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.stoch_period = stoch_period

        self.rsi = RSI(rsi_period)
        self.add_sub_indicator(self.rsi)

        self.smoothed_k = SMA(smoothing_period_k)
        self.add_managed_sequence(self.smoothed_k)

        self.values_d = SMA(smoothing_period_d)
        self.add_managed_sequence(self.values_d)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.rsi) < self.stoch_period:
            return None

        recent_rsi = self.rsi[-1 * self.stoch_period:]

        max_high = max(recent_rsi)
        min_low = min(recent_rsi)

        if max_high == min_low:
            k = 100.0
        else:
            k = 100.0 * (self.rsi[-1] - min_low) / (max_high - min_low)

        self.smoothed_k.add_input_value(k)

        smoothed_k = None
        if len(self.smoothed_k) > 0:
            smoothed_k = self.smoothed_k[-1]
            self.values_d.add_input_value(self.smoothed_k[-1])

        d = None
        if len(self.values_d) > 0:
            d = self.values_d[-1]

        return StochRSIVal(smoothed_k, d)
