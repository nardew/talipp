from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.ROC import ROC
from talipp.indicators.WMA import WMA
from talipp.input import SamplingPeriodType


class CoppockCurve(Indicator):
    """CoppockCurve.

    Input type: `float`

    Output type: `float`

    Args:
        fast_roc_period: Fast [ROC][talipp.indicators.ROC] period.
        slow_roc_period: Slow [ROC][talipp.indicators.ROC] period.
        wma_period: [WMA][talipp.indicators.WMA] period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, fast_roc_period: int,
                 slow_roc_period: int,
                 wma_period: int,
                 input_values: List[float] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.fast_roc = ROC(fast_roc_period)
        self.add_sub_indicator(self.fast_roc)

        self.slow_roc = ROC(slow_roc_period)
        self.add_sub_indicator(self.slow_roc)

        self.wma = WMA(wma_period)
        self.add_managed_sequence(self.wma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.fast_roc, 1) or not has_valid_values(self.slow_roc, 1):
            return None

        self.wma.add(self.slow_roc[-1] + self.fast_roc[-1])

        if not has_valid_values(self.wma, 1):
            return None

        return self.wma[-1]
