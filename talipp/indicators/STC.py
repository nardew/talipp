from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.MACD import MACD, MACDVal
from talipp.indicators.Stoch import Stoch, StochVal
from talipp.ohlcv import OHLCV


class STC(Indicator):
    """
    Schaff Trend Cycle

    Output: a list of floats
    """

    def __init__(self, fast_macd_period: int, slow_macd_period: int, stoch_period: int, stoch_smoothing_period:int, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        # use slow_macd_period for signal line as signal line is not relevant here
        self.macd = MACD(fast_macd_period, slow_macd_period, slow_macd_period)
        self.stoch_macd = Stoch(stoch_period, stoch_smoothing_period, input_indicator=self.macd, value_extractor=STC.macd_to_ohlcv)
        self.stoch_d = Stoch(stoch_period, stoch_smoothing_period, input_indicator=self.stoch_macd, value_extractor=STC.stoch_d_to_ohlcv)

        self.add_sub_indicator(self.macd)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.stoch_d) > 0 and self.stoch_d[-1].d is not None:
            return max(min(self.stoch_d[-1].d, 100), 0)
        else:
            return None

    @staticmethod
    def macd_to_ohlcv(macd_val: MACDVal) -> OHLCV:
        return OHLCV(macd_val.macd, macd_val.macd, macd_val.macd, macd_val.macd)

    @staticmethod
    def stoch_d_to_ohlcv(stoch_val: StochVal) -> OHLCV:
        return OHLCV(stoch_val.d, stoch_val.d, stoch_val.d, stoch_val.d)
