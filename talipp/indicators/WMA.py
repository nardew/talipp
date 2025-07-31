import numpy as np
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType


class WMA(Indicator):
    """Weighted Moving Average.

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

        self.denom_sum = period * (period + 1) / 2.0

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        # Convert input_values to a NumPy array for vectorized operations
        input_values_np = np.array(self.input_values[-self.period:])

        # Calculate weighted moving average using NumPy vectorized operations
        weights = np.arange(1, self.period + 1)
        wma = np.sum(input_values_np * weights) / self.denom_sum

        return wma
