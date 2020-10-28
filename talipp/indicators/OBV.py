from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class OBV(Indicator):
    """
    On Balance Volume

    Output: a list of floats
    """

    def __init__(self, input_values: List[OHLCV] = None):
        super().__init__()

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) == 1:
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