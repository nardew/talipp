from datetime import datetime
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType


class SMA(Indicator):
    """Simple Moving Average.

    Input type: `float`

    Output type: `float`

    Args:
        period: Period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 input_values: List[float] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None,
                 period_start: datetime = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling,
                         period_start=period_start)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if has_valid_values(self.input_values, self.period + 1):
            return self.output_values[-1] - \
                   (self.input_values[-self.period - 1] - self.input_values[-1]) / float(self.period)
        elif has_valid_values(self.input_values, self.period, exact=True):
            return float(sum(self.input_values[-self.period:])) / self.period
        else: # len(self.input_values) < self.period
            return None
