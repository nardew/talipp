from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators import ATR
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class NATR(Indicator):
    """Normalized Average True Range

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
        super(NATR, self).__init__(input_modifier=input_modifier,
                                   input_sampling=input_sampling)

        self.period = period
        self.atr = ATR(period)

        self.add_sub_indicator(self.atr)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.atr, 1):
            return None

        if self.input_values[-1].close == 0:
            return None

        return 100.0 * self.atr[-1] / self.input_values[-1].close
