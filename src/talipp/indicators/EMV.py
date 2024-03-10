from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV


class EMV(Indicator):
    """Ease of Movement.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        period: Period.
        volume_div: Volume divider.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 volume_div: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.SMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.period = period
        self.volume_div = volume_div

        self.emv_sma = MAFactory.get_ma(ma_type, period)
        self.add_managed_sequence(self.emv_sma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        value = self.input_values[-1]
        value2 = self.input_values[-2]
        if value.high != value.low:
            distance = (value.high + value.low) / 2.0 - (value2.high + value2.low) / 2.0
            box_ratio = (value.volume / float(self.volume_div)) / (value.high - value.low)
            emv = distance / box_ratio
        else:
            emv = 0.0

        self.emv_sma.add(emv)

        if not has_valid_values(self.emv_sma, 1):
            return None
        else:
            return self.emv_sma[-1]
