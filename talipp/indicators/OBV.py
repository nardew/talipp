from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ohlcv import OHLCV


class OBV(Indicator):
    """
    On Balance Volume

    Output: a list of floats
    """

    def __init__(self, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 1):
            return None
        elif has_valid_values(self.input_values, 1, exact=True):
            return self.input_values[0].volume
        else:
            value = self.input_values[-1]
            prev_value = self.input_values[-2]

            if value.close == prev_value.close:
                return self.output_values[-1]
            elif value.close > prev_value.close:
                return self.output_values[-1] + value.volume
            else:
                return self.output_values[-1] - value.volume
