from dataclasses import dataclass
from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators import BB, DonchianChannels, KeltnerChannels, SMA
from talipp.ohlcv import OHLCV, ValueExtractor


@dataclass
class TTMVal:
    # squeeze is on (=True) or off (=False
    squeeze: bool = None

    # histogram of the linear regression
    histogram: float = None


class TTM(Indicator):
    """
    TTM Squeeze

    Output: a list of TTMVal
    """

    def __init__(self, period: int, bb_std_dev_mult: float = 2, kc_atr_mult: float = 1.5,
                 input_values: List[OHLCV] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period

        self.bb = BB(period, bb_std_dev_mult, value_extractor = ValueExtractor.extract_close)
        self.dc = DonchianChannels(period)
        self.kc = KeltnerChannels(period, period, kc_atr_mult, kc_atr_mult)
        self.sma = SMA(period, value_extractor = ValueExtractor.extract_close)

        self.add_sub_indicator(self.bb)
        self.add_sub_indicator(self.dc)
        self.add_sub_indicator(self.kc)
        self.add_sub_indicator(self.sma)

        self.deltas = []
        self.add_managed_sequence(self.deltas)

        # pre-compute values for linear regression
        self.mean_x = sum(range(self.period)) / float(self.period)
        self.denom = 0
        for x in range(self.period):
            self.denom += (x - self.mean_x) ** 2

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.bb) < 1 or len(self.kc) < 1:
            return None

        # squeeze is on if BB is entirely encompassed in KC
        squeeze = self.bb[-1].ub < self.kc[-1].ub and self.bb[-1].lb > self.kc[-1].lb

        if len(self.sma) > 0 and len(self.dc) > 0:
            self.deltas.append(self.input_values[-1].close - (self.dc[-1].cb + self.sma[-1]) / 2.0)

        hist = None
        if len(self.deltas) >= self.period:
            # calculate linear regression y = ax + b
            mean_y = sum(self.deltas[-self.period:]) / float(self.period)

            numer = 0
            for x, y in zip(range(self.period), self.deltas[-self.period:]):
                numer += (x - self.mean_x) * (y - mean_y)
            a = numer / self.denom
            b = mean_y - (a * self.mean_x)

            hist = a * (self.period - 1) + b

        return TTMVal(squeeze, hist)