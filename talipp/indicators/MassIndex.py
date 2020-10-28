from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.EMA import EMA
from talipp.ohlcv import OHLCV


class MassIndex(Indicator):
    """
    Mass Index

    Output: a list of floats
    """

    def __init__(self, ema_period: int, ema_ema_period: int, ema_ratio_period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.ema_ratio_period = ema_ratio_period

        self.ema = EMA(ema_period)
        self.ema_ema = EMA(ema_ema_period)
        self.ema_ratio = []

        self.add_managed_sequence(self.ema)
        self.add_managed_sequence(self.ema_ema)
        self.add_managed_sequence(self.ema_ratio)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        self.ema.add_input_value(value.high - value.low)

        if not self.ema.has_output_value():
            return None

        self.ema_ema.add_input_value(self.ema[-1])

        if not self.ema_ema.has_output_value():
            return None

        self.ema_ratio.append(self.ema[-1] / float(self.ema_ema[-1]))

        if len(self.ema_ratio) < self.ema_ratio_period:
            return None

        return sum(self.ema_ratio[-self.ema_ratio_period:])
