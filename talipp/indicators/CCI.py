from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.MeanDev import MeanDev
from talipp.ohlcv import OHLCV


class CCI(Indicator):
    """
    Commodity Channel Index

    Output: a list of OHLCV objects
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.mean_dev = MeanDev(period)
        self.add_managed_sequence(self.mean_dev)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        typical_price = (value.high + value.low + value.close) / 3.0

        self.mean_dev.add_input_value(typical_price)

        if len(self.mean_dev) < 1:
            return None

        # take SMA(typical_price) directly form MeanDev since it is already calculating it in the background
        return (typical_price - self.mean_dev.sma[-1]) / (0.015 * self.mean_dev[-1])