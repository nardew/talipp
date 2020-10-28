import enum
from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class SARTrend(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()


@dataclass
class ParabolicSARVal:
    value: float = None
    trend: SARTrend = None
    ep: float = None
    accel_factor: float = None


class ParabolicSAR(Indicator):
    """
    Parabolic Stop And Reverse

    Output: a list of ParabolicSARVal
    """

    SAR_INIT_LEN = 5

    def __init__(self, init_accel_factor: float, accel_factor_inc: float, max_accel_factor: float, input_values: List[OHLCV] = None):
        super().__init__()

        self.init_accel_factor = init_accel_factor
        self.accel_factor_inc = accel_factor_inc
        self.max_accel_factor = max_accel_factor

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < ParabolicSAR.SAR_INIT_LEN:
            return None
        elif len(self.input_values) == ParabolicSAR.SAR_INIT_LEN:
            min_low = min(self.input_values[-ParabolicSAR.SAR_INIT_LEN:], key = lambda x: x.low).low
            max_high = max(self.input_values[-ParabolicSAR.SAR_INIT_LEN:], key = lambda x: x.high).high

            return ParabolicSARVal(min_low, SARTrend.UP, max_high, self.init_accel_factor)
        else:
            prev_sar: ParabolicSARVal = self.output_values[-1]

            new_sar_val = prev_sar.value + prev_sar.accel_factor * (prev_sar.ep - prev_sar.value)
            new_trend = prev_sar.trend
            new_ep = prev_sar.ep
            new_accel_factor = prev_sar.accel_factor

            # if new SAR overlaps last lows/highs (depending on the trend), cut it at that value
            if prev_sar.trend == SARTrend.UP and new_sar_val > min(self.input_values[-2].low, self.input_values[-3].low):
                new_sar_val = min(self.input_values[-2].low, self.input_values[-3].low)
            elif prev_sar.trend == SARTrend.DOWN and new_sar_val < max(self.input_values[-2].high, self.input_values[-3].high):
                new_sar_val = max(self.input_values[-2].high, self.input_values[-3].high)

            # update extreme point
            if prev_sar.trend == SARTrend.UP and self.input_values[-1].high > prev_sar.ep:
                new_ep = self.input_values[-1].high
            elif prev_sar.trend == SARTrend.DOWN and self.input_values[-1].low < prev_sar.ep:
                new_ep = self.input_values[-1].low

            # if extreme point was updated, increase acceleration factor
            if new_ep != prev_sar.ep:
                new_accel_factor = new_accel_factor + self.accel_factor_inc
                if new_accel_factor > self.max_accel_factor:
                    new_accel_factor = self.max_accel_factor

            # check if trend is reversed and initialize new initial values
            if prev_sar.trend == SARTrend.UP and new_sar_val > self.input_values[-1].low:
                new_sar_val = max(prev_sar.ep, self.input_values[-1].high)
                new_ep = self.input_values[-1].low
                new_trend = SARTrend.DOWN
                new_accel_factor = self.init_accel_factor
            elif prev_sar.trend == SARTrend.DOWN and new_sar_val < self.input_values[-1].high:
                new_sar_val = min(prev_sar.ep, self.input_values[-1].low)
                new_ep = self.input_values[-1].high
                new_trend = SARTrend.UP
                new_accel_factor = self.init_accel_factor

            return ParabolicSARVal(new_sar_val, new_trend, new_ep, new_accel_factor)
