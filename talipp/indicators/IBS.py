from datetime import datetime
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class IBS(Indicator):
    """Internal Bar Strength.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
        period_start: Period start for sampling (optional)
    """

    def __init__(self,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None,
                 period_start: datetime = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling,
                         period_start=period_start)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values):
            return None

        candle: OHLCV = self.input_values[-1]
        return (candle.close - candle.low) / (candle.high - candle.low)
