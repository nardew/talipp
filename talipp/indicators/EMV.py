from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.SMA import SMA
from talipp.ohlcv import OHLCV


class EMV(Indicator):
    """
    Ease of Movement

    Output: a list of floats
    """

    def __init__(self, period: int, volume_div: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.period = period
        self.volume_div = volume_div

        self.emv_sma = SMA(self.period)
        self.add_managed_sequence(self.emv_sma)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        value = self.input_values[-1]
        value2 = self.input_values[-2]
        if value.high != value.low:
            distance = (value.high + value.low) / 2.0 - (value2.high + value2.low) / 2.0
            box_ratio = (value.volume / float(self.volume_div)) / (value.high - value.low)
            emv = distance / box_ratio
        else:
            emv = 0.0

        self.emv_sma.add_input_value(emv)

        if len(self.emv_sma) < 1:
            return None
        else:
            return self.emv_sma[-1]