from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.ROC import ROC
from talipp.indicators.WMA import WMA


class CoppockCurve(Indicator):
    """
    CoppockCurve

    Output: a list of floats
    """

    def __init__(self, fast_roc_period: int, slow_roc_period: int, wma_period: int,
                 input_values: List[float] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

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
