from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.ATR import ATR
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV, ValueExtractor


@dataclass
class KeltnerChannelsVal:
    """`KeltnerChannels` output type.

    Args:
        lb: Lower band.
        cb: Central band.
        ub: Upper band.
    """

    lb: float = None
    cb: float = None
    ub: float = None


class KeltnerChannels(Indicator):
    """Keltner Channels.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [KeltnerChannelsVal][talipp.indicators.KeltnerChannels.KeltnerChannelsVal]

    Args:
        ma_period: Moving average period.
        atr_period: [ATR][talipp.indicators.ATR] period.
        atr_mult_up: Upper band multiplier.
        atr_mult_down: Lower band multiplier.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
    """

    def __init__(self, ma_period: int,
                 atr_period: int,
                 atr_mult_up: float,
                 atr_mult_down: float,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.EMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=KeltnerChannelsVal,
                         input_sampling=input_sampling)

        self.atr_mult_up = atr_mult_up
        self.atr_mult_down = atr_mult_down

        self.atr = ATR(atr_period)
        self.cb = MAFactory.get_ma(ma_type, ma_period, input_modifier=ValueExtractor.extract_close)

        self.add_sub_indicator(self.cb)
        self.add_sub_indicator(self.atr)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.cb, 1) or not has_valid_values(self.atr, 1):
            return None

        return KeltnerChannelsVal(self.cb[-1] - self.atr_mult_down * self.atr[-1],
                                  self.cb[-1],
                                  self.cb[-1] + self.atr_mult_up * self.atr[-1])
