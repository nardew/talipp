from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.ATR import ATR
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.StdDev import StdDev
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV, ValueExtractor


@dataclass
class SFXVal:
    """`SFX` output type.

    Args:
        atr: `ATR` value.
        std_dev: Standard deviation.
        ma_std_dev: Standard deviation moving average.
    """

    atr: float = None
    std_dev: float = None
    ma_std_dev: float = None


class SFX(Indicator):
    """SFX.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [SFXVal][talipp.indicators.SFX.SFXVal]

    Args:
        atr_period: [ATR][talipp.indicators.ATR] period.
        std_dev_period: [Standard deviation][talipp.indicators.StdDev] period.
        std_dev_period: Standard deviation moving average period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
    """

    def __init__(self, atr_period: int,
                 std_dev_period: int,
                 std_dev_smoothing_period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.SMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=SFXVal,
                         input_sampling=input_sampling)

        self.atr = ATR(atr_period)
        self.std_dev = StdDev(std_dev_period, input_modifier=ValueExtractor.extract_close)
        self.ma_std_dev = MAFactory.get_ma(ma_type, std_dev_smoothing_period, input_indicator=self.std_dev)

        self.add_sub_indicator(self.atr)
        self.add_sub_indicator(self.std_dev)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if has_valid_values(self.atr, 1):
            atr = self.atr[-1]
        else:
            atr = None

        if has_valid_values(self.std_dev, 1):
            std_dev = self.std_dev[-1]
        else:
            std_dev = None

        if has_valid_values(self.ma_std_dev, 1):
            ma_std_dev = self.ma_std_dev[-1]
        else:
            ma_std_dev = None

        return SFXVal(atr, std_dev, ma_std_dev)
