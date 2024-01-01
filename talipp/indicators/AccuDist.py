from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ohlcv import OHLCV


class AccuDist(Indicator):
    """
    Accumulation and Distribution

    Output: a list of floats
    """

    def __init__(self, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]

        if value.high != value.low:
            mfm = ((value.close - value.low) - (value.high - value.close)) / float(value.high - value.low)
            mfv = mfm * value.volume
        else:
            # in case high and low are equal (and hence division by zero above), return None
            return None

        if not has_valid_values(self.output_values):
            return mfv
        else:
            return self.output_values[-1] + mfv
