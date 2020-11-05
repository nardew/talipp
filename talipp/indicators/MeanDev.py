from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.SMA import SMA


class MeanDev(Indicator):
    """
    Mean Deviation

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.sma = SMA(period)
        self.add_sub_indicator(self.sma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.sma) < 1:
            return None

        return sum(map(lambda x: abs(x - self.sma[-1]), self.input_values[-self.period:])) / float(self.period)
