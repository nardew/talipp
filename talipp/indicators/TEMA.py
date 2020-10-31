from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.EMA import EMA


class TEMA(Indicator):
    """
    Triple Exponential Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period

        self.ema = EMA(period)
        self.add_sub_indicator(self.ema)

        self.ema_ema = EMA(period)
        self.ema_ema_ema = EMA(period)

        self.add_managed_sequence(self.ema_ema)
        self.add_managed_sequence(self.ema_ema_ema)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not self.ema.has_output_value():
            return None

        self.ema_ema.add_input_value(self.ema[-1])

        if not self.ema_ema.has_output_value():
            return None

        self.ema_ema_ema.add_input_value(self.ema_ema[-1])

        if not self.ema_ema_ema.has_output_value():
            return None

        return 3.0 * self.ema[-1] - 3.0 * self.ema_ema[-1] + self.ema_ema_ema[-1]
