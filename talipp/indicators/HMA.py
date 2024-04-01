from math import sqrt
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.WMA import WMA
from talipp.input import SamplingPeriodType


class HMA(Indicator):
    """Hull Moving Average.

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

        self.wma = WMA(period)
        self.wma2 = WMA(int(period / 2))
        self.hma = WMA(int(sqrt(period)))

        self.add_sub_indicator(self.wma)
        self.add_sub_indicator(self.wma2)
        self.add_managed_sequence(self.hma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.wma, int(sqrt(self.period))):
            return None

        self.hma.add(2.0 * self.wma2[-1] - self.wma[-1])

        if not has_valid_values(self.hma, 1):
            return None

        return self.hma[-1]
