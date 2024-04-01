from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.EMA import EMA
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType


class DEMA(Indicator):
    """Double Exponential Moving Average.

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
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.period = period

        self.ema = EMA(period)
        self.add_sub_indicator(self.ema)

        self.ema_ema = EMA(period)
        self.add_managed_sequence(self.ema_ema)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.ema, 1):
            return None

        self.ema_ema.add(self.ema[-1])

        if not has_valid_values(self.ema_ema, 1):
            return None

        return 2.0 * self.ema[-1] - self.ema_ema[-1]
