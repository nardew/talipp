from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ohlcv import OHLCV


@dataclass
class DonchianChannelsVal:
    # lower band
    lb: float = None

    # central band
    cb: float = None

    # upper band
    ub: float = None


class DonchianChannels(Indicator):
    """
    Donchian Channels

    Output: a list of DonnchianChannelsVal
    """
    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None):
        super().__init__(input_modifier=input_modifier, output_value_type=DonchianChannelsVal)

        self.period = period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        max_high = max(self.input_values[-self.period:], key = lambda x: x.high).high
        min_low = min(self.input_values[-self.period:], key = lambda x: x.low).low

        return DonchianChannelsVal(min_low,
                                   (max_high + min_low) / 2.0,
                                   max_high)
