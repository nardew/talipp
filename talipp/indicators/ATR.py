from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.TrueRange import TrueRange
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class ATR(Indicator):
    """Average True Range

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
        super(ATR, self).__init__(input_modifier=input_modifier,
                                  input_sampling=input_sampling)

        self.period = period

        self._tr = TrueRange()
        self.add_sub_indicator(self._tr)

        self.tr = []

        self.add_managed_sequence(self.tr)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        tr = self._tr.output_values[-1]
        if has_valid_values(self.input_values, 1, exact=True):
            self.tr.append(tr)
        else:
            self.tr.append(tr)

        if len(self.input_values) < self.period:
            return None
        elif len(self.input_values) == self.period:
            return sum(self.tr) / self.period
        else:
            return (self.output_values[-1] * (self.period - 1) + self.tr[-1]) / self.period
