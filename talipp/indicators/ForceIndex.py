from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.EMA import EMA
from talipp.ohlcv import OHLCV


class ForceIndex(Indicator):
    """
    Force Index

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.ema = EMA(period)
        self.add_managed_sequence(self.ema)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        self.ema.add_input_value((self.input_values[-1].close - self.input_values[-2].close) * self.input_values[-1].volume)

        if len(self.ema) > 1:
            return self.ema[-1]
        else:
            return None