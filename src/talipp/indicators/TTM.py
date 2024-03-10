from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators import BB, DonchianChannels, KeltnerChannels
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV, ValueExtractor


@dataclass
class TTMVal:
    """`TTM` output type.

    Args:
        squeeze: `True` if squeeze is on, otherwise `False`.
        histogram: Histogram of the linear regression.
    """

    squeeze: bool = None
    histogram: float = None


class TTM(Indicator):
    """TTM Squeeze.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [TTMVal][talipp.indicators.TTM.TTMVal]

    Args:
        period: Period.
        bb_std_dev_mult: [BB][talipp.indicators.BB] standard deviation multiplier.
        kc_atr_mult: [KeltnerChannels][talipp.indicators.KeltnerChannels] [ATR][talipp.indicators.ATR] multiplier.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 bb_std_dev_mult: float = 2,
                 kc_atr_mult: float = 1.5,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.SMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=TTMVal,
                         input_sampling=input_sampling)

        self.period = period

        self.bb = BB(period, bb_std_dev_mult, input_modifier=ValueExtractor.extract_close)
        self.dc = DonchianChannels(period)
        self.kc = KeltnerChannels(period, period, kc_atr_mult, kc_atr_mult)
        self.ma = MAFactory.get_ma(ma_type, period, input_modifier=ValueExtractor.extract_close)

        self.add_sub_indicator(self.bb)
        self.add_sub_indicator(self.dc)
        self.add_sub_indicator(self.kc)
        self.add_sub_indicator(self.ma)

        self.deltas = []
        self.add_managed_sequence(self.deltas)

        # pre-compute values for linear regression
        self.mean_x = sum(range(self.period)) / float(self.period)
        self.denom = 0
        for x in range(self.period):
            self.denom += (x - self.mean_x) ** 2

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.bb, 1) or not has_valid_values(self.kc, 1):
            return None

        # squeeze is on if BB is entirely encompassed in KC
        squeeze = self.bb[-1].ub < self.kc[-1].ub and self.bb[-1].lb > self.kc[-1].lb

        if has_valid_values(self.ma, 1) and has_valid_values(self.dc, 1):
            self.deltas.append(self.input_values[-1].close - (self.dc[-1].cb + self.ma[-1]) / 2.0)

        hist = None
        if has_valid_values(self.deltas, self.period):
            # calculate linear regression y = ax + b
            mean_y = sum(self.deltas[-self.period:]) / float(self.period)

            numer = 0
            for x, y in zip(range(self.period), self.deltas[-self.period:]):
                numer += (x - self.mean_x) * (y - mean_y)
            a = numer / self.denom
            b = mean_y - (a * self.mean_x)

            hist = a * (self.period - 1) + b

        return TTMVal(squeeze, hist)
