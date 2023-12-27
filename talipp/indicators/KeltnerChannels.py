from dataclasses import dataclass
from typing import List, Any

from talipp.indicators.ATR import ATR
from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV, ValueExtractor


@dataclass
class KeltnerChannelsVal:
    # lower band
    lb: float = None

    # central band
    cb: float = None

    # upper band
    ub: float = None


class KeltnerChannels(Indicator):
    """
    Keltner Channels

    Output: a list of KeltnerChannelsVal
    """

    def __init__(self, ma_period: int, atr_period: int, atr_mult_up: float, atr_mult_down: float, input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None, value_extractor: ValueExtractorType = None,
                 ma_type: MAType = MAType.EMA):
        super().__init__(value_extractor = value_extractor)

        self.atr_mult_up = atr_mult_up
        self.atr_mult_down = atr_mult_down

        self.atr = ATR(atr_period)
        self.cb = MAFactory.get_ma(ma_type, ma_period, value_extractor=ValueExtractor.extract_close)

        self.add_sub_indicator(self.cb)
        self.add_sub_indicator(self.atr)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.cb) < 1 or len(self.atr) < 1:
            return None

        return KeltnerChannelsVal(self.cb[-1] - self.atr_mult_down * self.atr[-1],
                                  self.cb[-1],
                                  self.cb[-1] + self.atr_mult_up * self.atr[-1])
