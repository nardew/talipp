from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ohlcv import OHLCV


class ATR(Indicator):
    """
    Average True Range

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super(ATR, self).__init__()

        self.period = period
        self.tr = []

        self.add_managed_sequence(self.tr)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        high = self.input_values[-1].high
        low = self.input_values[-1].low

        if has_valid_values(self.input_values, 1, exact=True):
            self.tr.append(high - low)
        else:
            close2 = self.input_values[-2].close
            self.tr.append(max(
                high - low,
                abs(high - close2),
                abs(low - close2),
            ))

        if len(self.input_values) < self.period:
            return None
        elif len(self.input_values) == self.period:
            return sum(self.tr) / self.period
        else:
            return (self.output_values[-1] * (self.period - 1) + self.tr[-1]) / self.period
