from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.EMA import EMA
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType


class TRIX(Indicator):
    """TRIX.

    Input type: `float`

    Output type: `float`

    Args:
        period: Period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 input_values: List[float] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.period = period

        self.ema1 = EMA(period)
        self.ema2 = EMA(period, input_indicator = self.ema1)
        self.ema3 = EMA(period, input_indicator = self.ema2)

        self.add_sub_indicator(self.ema1)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.ema3, 2):
            return None

        return 10000.0 * (self.ema3[-1] - self.ema3[-2]) / self.ema3[-2]
