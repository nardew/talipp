from math import sqrt, log
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class RogersSatchell(Indicator):
    """Rogers-Satchell volatility indicator.

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

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        s = 0.0
        for ohlcv in self.input_values[-self.period:]:
            s += log(float(ohlcv.high) / ohlcv.close) * log(float(ohlcv.high) / ohlcv.open) + log(float(ohlcv.low) / ohlcv.close) * log(float(ohlcv.low) / ohlcv.open)

        return sqrt(s / self.period)
