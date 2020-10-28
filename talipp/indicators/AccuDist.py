from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class AccuDist(Indicator):
    """
    Accumulation and Distribution

    Output: a list of floats
    """

    def __init__(self, input_values: List[OHLCV] = None):
        super().__init__()

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]

        if value.high != value.low:
            mfm = ((value.close - value.low) - (value.high - value.close)) / float(value.high - value.low)
            mfv = mfm * value.volume
        else:
            # in case high and low are equal (and hence division by zero above), return previous value if exists, otherwise
            # return None
            if self.has_output_value():
                return self.output_values[-1]
            else:
                return None

        if not self.has_output_value():
            return mfv
        else:
            return self.output_values[-1] + mfv
