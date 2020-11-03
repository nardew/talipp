from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.EMA import EMA


class TRIX(Indicator):
    """
    TRIX

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.ema1 = EMA(period)
        self.ema2 = EMA(period, input_indicator = self.ema1)
        self.ema3 = EMA(period, input_indicator = self.ema2)

        self.add_sub_indicator(self.ema1)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.ema3) < 2:
            return None

        return 10000.0 * (self.ema3[-1] - self.ema3[-2]) / self.ema3[-2]