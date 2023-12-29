from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.RSI import RSI
from talipp.ma import MAType, MAFactory


@dataclass
class StochRSIVal:
    k: float = None
    d: float = None


class StochRSI(Indicator):
    """
    Stochastic RSI

    Output: a list of StochRSIVal
    """

    def __init__(self, rsi_period: int, stoch_period: int, k_smoothing_period: int, d_smoothing_period: int,
                 input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None,
                 ma_type: MAType = MAType.SMA):
        super().__init__(value_extractor = value_extractor, output_value_type=StochRSIVal)

        self.stoch_period = stoch_period

        self.rsi = RSI(rsi_period)
        self.add_sub_indicator(self.rsi)

        self.smoothed_k = MAFactory.get_ma(ma_type, k_smoothing_period)
        self.add_managed_sequence(self.smoothed_k)

        self.values_d = MAFactory.get_ma(ma_type, d_smoothing_period)
        self.add_managed_sequence(self.values_d)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.rsi, self.stoch_period):
            return None

        recent_rsi = self.rsi[-self.stoch_period:]

        max_high = max(recent_rsi)
        min_low = min(recent_rsi)

        if max_high == min_low:
            k = 100.0
        else:
            k = 100.0 * (self.rsi[-1] - min_low) / (max_high - min_low)

        self.smoothed_k.add_input_value(k)
        self.values_d.add_input_value(self.smoothed_k[-1])

        return StochRSIVal(self.smoothed_k[-1], self.values_d[-1])
