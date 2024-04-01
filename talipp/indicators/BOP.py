from typing import List, Any

from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class BOP(Indicator):
    """Balance Of Power.

    Input type: `float`

    Output type: `float`

    Args:
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        if value.high != value.low:
            return (value.close - value.open) / float(value.high - value.low)
        else:
            return None
