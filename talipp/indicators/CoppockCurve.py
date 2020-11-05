from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.ROC import ROC
from talipp.indicators.WMA import WMA


class CoppockCurve(Indicator):
    """
    CoppockCurve

    Output: a list of floats
    """

    def __init__(self, fast_roc_period: int, slow_roc_period: int, wma_period: int,
                 input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.fast_roc = ROC(fast_roc_period)
        self.add_sub_indicator(self.fast_roc)

        self.slow_roc = ROC(slow_roc_period)
        self.add_sub_indicator(self.slow_roc)

        self.wma = WMA(wma_period)
        self.add_managed_sequence(self.wma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.fast_roc) < 1 or len(self.slow_roc) < 1:
            return None

        self.wma.add_input_value(self.slow_roc[-1] + self.fast_roc[-1])

        if len(self.wma) < 1:
            return None

        return self.wma[-1]