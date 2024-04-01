from typing import List, Any

from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class VWAP(Indicator):
    """Volume Weighted Average Price.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.sum_price_vol = []
        self.sum_vol = []

        self.add_managed_sequence(self.sum_price_vol)
        self.add_managed_sequence(self.sum_vol)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        # initialize sums
        if len(self.sum_price_vol) == 0:
            self.sum_price_vol.append(0.0)
            self.sum_vol.append(0.0)

        value = self.input_values[-1]
        typical_price = (value.high + value.low + value.close) / 3.0

        self.sum_price_vol.append(self.sum_price_vol[-1] + value.volume * typical_price)
        self.sum_vol.append(self.sum_vol[-1] + value.volume)

        if self.sum_vol[-1] != 0:
            return self.sum_price_vol[-1] / self.sum_vol[-1]
        else:
            return None
