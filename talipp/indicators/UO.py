from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class UO(Indicator):
    """
    Ultimate Oscillator

    Output: a list of floats
    """

    def __init__(self, fast_period: int, mid_period: int, slow_period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.fast_period = fast_period
        self.mid_period = mid_period
        self.slow_period = slow_period

        self.buy_press = []
        self.true_range = []

        self.add_managed_sequence(self.buy_press)
        self.add_managed_sequence(self.true_range)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        value = self.input_values[-1]
        prev_value = self.input_values[-2]

        self.buy_press.append(value.close - min(value.low, prev_value.close))
        self.true_range.append(max(value.high, prev_value.close) - min(value.low, prev_value.close))

        if len(self.buy_press) < self.slow_period:
            return None

        avg_fast = sum(self.buy_press[-self.fast_period:]) / float(sum(self.true_range[-self.fast_period:]))
        avg_mid = sum(self.buy_press[-self.mid_period:]) / float(sum(self.true_range[-self.mid_period:]))
        avg_slow = sum(self.buy_press[-self.slow_period:]) / float(sum(self.true_range[-self.slow_period:]))

        return 100.0 * (4.0 * avg_fast + 2.0 * avg_mid + avg_slow) / 7.0
