from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.EMA import EMA
from talipp.indicators.Indicator import Indicator, ValueExtractorType


class DEMA(Indicator):
    """
    Double Exponential Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.ema = EMA(period)
        self.add_sub_indicator(self.ema)

        self.ema_ema = EMA(period)
        self.add_managed_sequence(self.ema_ema)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.ema, 1):
            return None

        self.ema_ema.add_input_value(self.ema[-1])

        if not has_valid_values(self.ema_ema, 1):
            return None

        return 2.0 * self.ema[-1] - self.ema_ema[-1]
