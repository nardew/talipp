from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class UO(Indicator):
    """Ultimate Oscillator.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        fast_period: Fast period.
        mid_period: Mid period.
        slow_period: Slow period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, fast_period: int,
                 mid_period: int,
                 slow_period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.fast_period = fast_period
        self.mid_period = mid_period
        self.slow_period = slow_period

        self.buy_press = []
        self.true_range = []

        self.add_managed_sequence(self.buy_press)
        self.add_managed_sequence(self.true_range)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        value = self.input_values[-1]
        prev_value = self.input_values[-2]

        self.buy_press.append(value.close - min(value.low, prev_value.close))
        self.true_range.append(max(value.high, prev_value.close) - min(value.low, prev_value.close))

        if not has_valid_values(self.buy_press, self.slow_period):
            return None

        fast_sum = sum(self.true_range[-self.fast_period:])
        mid_sum = sum(self.true_range[-self.mid_period:])
        slow_sum = sum(self.true_range[-self.slow_period:])

        if fast_sum == 0 or mid_sum == 0 or slow_sum == 0:
            return None

        avg_fast = sum(self.buy_press[-self.fast_period:]) / float(fast_sum)
        avg_mid = sum(self.buy_press[-self.mid_period:]) / float(mid_sum)
        avg_slow = sum(self.buy_press[-self.slow_period:]) / float(slow_sum)

        return 100.0 * (4.0 * avg_fast + 2.0 * avg_mid + avg_slow) / 7.0
