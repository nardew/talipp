from dataclasses import dataclass
from typing import List, Any

from talipp.indicators.ATR import ATR
from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.StdDev import StdDev
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV, ValueExtractor


@dataclass
class SFXVal:
    atr: float = None
    std_dev: float = None
    ma_std_dev: float = None


class SFX(Indicator):
    """
    Output: A list of SFXVal
    """

    def __init__(self, atr_period: int, std_dev_period: int, std_dev_smoothing_period: int, input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None, value_extractor: ValueExtractorType = None,
                 ma_type: MAType = MAType.SMA):
        super().__init__(value_extractor = value_extractor)

        self.atr = ATR(atr_period)
        self.std_dev = StdDev(std_dev_period, value_extractor = ValueExtractor.extract_close)
        self.ma_std_dev = MAFactory.get_ma(ma_type, std_dev_smoothing_period)

        self.add_sub_indicator(self.atr)
        self.add_sub_indicator(self.std_dev)

        self.add_managed_sequence(self.ma_std_dev)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.std_dev) > 0:
            self.ma_std_dev.add_input_value(self.std_dev[-1])

        if len(self.atr) > 0:
            atr = self.atr[-1]
        else:
            atr = None

        if len(self.std_dev) > 0:
            std_dev = self.std_dev[-1]
        else:
            std_dev = None

        if len(self.ma_std_dev) > 0:
            sma_std_dev = self.ma_std_dev[-1]
        else:
            sma_std_dev = None

        return SFXVal(atr, std_dev, sma_std_dev)
