from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV


class MassIndex(Indicator):
    """Mass Index.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        ma_period: Moving average period.
        ma_ma_period: Moving average period of moving average.
        ma_ratio_period: Moving averages ration period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
    """

    def __init__(self, ma_period: int,
                 ma_ma_period: int,
                 ma_ratio_period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.EMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.ma_ratio_period = ma_ratio_period

        self.ma = MAFactory.get_ma(ma_type, ma_period)
        self.ma_ma = MAFactory.get_ma(ma_type, ma_ma_period)
        self.ma_ratio = []

        self.add_managed_sequence(self.ma)
        self.add_managed_sequence(self.ma_ma)
        self.add_managed_sequence(self.ma_ratio)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        self.ma.add(value.high - value.low)

        if not has_valid_values(self.ma, 1):
            return None

        self.ma_ma.add(self.ma[-1])

        if not has_valid_values(self.ma_ma, 1):
            return None

        self.ma_ratio.append(self.ma[-1] / float(self.ma_ma[-1]))

        if not has_valid_values(self.ma_ratio, self.ma_ratio_period):
            return None

        return sum(self.ma_ratio[-self.ma_ratio_period:])
