from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.MeanDev import MeanDev
from talipp.ohlcv import OHLCV


class CCI(Indicator):
    """
    Commodity Channel Index

    Output: a list of OHLCV objects
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.mean_dev = MeanDev(period)
        self.add_managed_sequence(self.mean_dev)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        typical_price = (value.high + value.low + value.close) / 3.0

        self.mean_dev.add(typical_price)

        if not has_valid_values(self.mean_dev, 1):
            return None

        # take SMA(typical_price) directly form MeanDev since it is already calculating it in the background
        return (typical_price - self.mean_dev.ma[-1]) / (0.015 * self.mean_dev[-1])
