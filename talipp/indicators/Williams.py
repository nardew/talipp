from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class Williams(Indicator):
    """Williams %R.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        period: Period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.period = period

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
            if has_valid_values(self.output_values, 1):
                return self.output_values[-1]
            else:
                return None

        return -100.0 * (max_high - self.input_values[-1].close) / (max_high - min_low)
