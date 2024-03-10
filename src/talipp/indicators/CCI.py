from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.MeanDev import MeanDev
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class CCI(Indicator):
    """Commodity Channel Index.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        period: Period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.mean_dev = MeanDev(period)
        self.add_managed_sequence(self.mean_dev)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        typical_price = (value.high + value.low + value.close) / 3.0

        self.mean_dev.add(typical_price)

        if not has_valid_values(self.mean_dev, 1):
            return None

        # take SMA(typical_price) directly from MeanDev since it is already calculating it in the background
        return (typical_price - self.mean_dev.ma[-1]) / (0.015 * self.mean_dev[-1])
