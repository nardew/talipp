from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.indicators.EMA import EMA


@dataclass
class MACDVal:
    macd: float = None
    signal: float = None
    histogram: float = None


class MACD(Indicator):
    """
    Moving Average Convergence Divergence

    Output: a list of MACDVal
    """

    def __init__(self, fast_period: int, slow_period: int, signal_period: int, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.ema_fast = EMA(fast_period)
        self.ema_slow = EMA(slow_period)
        self.signal_line = EMA(signal_period)

        self.add_sub_indicator(self.ema_fast)
        self.add_sub_indicator(self.ema_slow)
        self.add_managed_sequence(self.signal_line)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.ema_fast) > 0 and len(self.ema_slow) > 0:
            macd = self.ema_fast[-1] - self.ema_slow[-1]
            self.signal_line.add_input_value(macd)

            if len(self.signal_line) > 0:
                signal = self.signal_line[-1]
            else:
                signal = None

            histogram = None
            if macd is not None and signal is not None:
                histogram = macd - signal

            return MACDVal(macd, signal, histogram)
        else:
            return None
