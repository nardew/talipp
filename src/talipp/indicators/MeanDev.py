from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory


class MeanDev(Indicator):
    """Mean Deviation.

    Input type: `float`

    Output type: `float`

    Args:
        period: Moving average period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 input_values: List[float] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.SMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.period = period

        self.ma = MAFactory.get_ma(ma_type, period)
        self.add_sub_indicator(self.ma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.ma, 1):
            return None

        return sum(map(lambda x: abs(x - self.ma[-1]), self.input_values[-self.period:])) / float(self.period)
