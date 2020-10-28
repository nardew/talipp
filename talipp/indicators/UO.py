from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class UO(Indicator):
    """
    Ultimate Oscillator

    Output: a list of floats
    """

    def __init__(self, period_fast: int, period_mid: int, period_slow: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.period_fast = period_fast
        self.period_mid = period_mid
        self.period_slow = period_slow

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

        if len(self.buy_press) < self.period_slow:
            return None

        avg_fast = sum(self.buy_press[-self.period_fast:]) / float(sum(self.true_range[-self.period_fast:]))
        avg_mid = sum(self.buy_press[-self.period_mid:]) / float(sum(self.true_range[-self.period_mid:]))
        avg_slow = sum(self.buy_press[-self.period_slow:]) / float(sum(self.true_range[-self.period_slow:]))

        return 100.0 * (4.0 * avg_fast + 2.0 * avg_mid + avg_slow) / 7.0
