from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class TrueRange(Indicator):
    """True Range

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super(TrueRange, self).__init__(input_modifier=input_modifier,
                                  input_sampling=input_sampling)

        self._bars = None, None

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        high = self.input_values[-1].high
        low = self.input_values[-1].low

        if has_valid_values(self.input_values, 1, exact=True):
            return high - low
        else:
            close2 = self.input_values[-2].close
            return max(
                high - low,
                abs(high - close2),
                abs(low - close2),
            )
