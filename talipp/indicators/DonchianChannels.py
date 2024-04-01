from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


@dataclass
class DonchianChannelsVal:
    """`DonchianChannels` output type.

    Args:
        lb: Lower band.
        cb: Central band.
        ub: Upper band.
    """

    lb: float = None
    cb: float = None
    ub: float = None


class DonchianChannels(Indicator):
    """Donchian Channels.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [DonchianChannelsVal][talipp.indicators.DonchianChannels.DonchianChannelsVal]

    Args:
        period: Period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """
    def __init__(self, period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=DonchianChannelsVal,
                         input_sampling=input_sampling)

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
