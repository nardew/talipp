import enum
from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class SARTrend(enum.Enum):
    """`ParabolicSAR` trend."""

    UP = enum.auto()
    """Up trend."""

    DOWN = enum.auto()
    """Down trend."""


@dataclass
class ParabolicSARVal:
    """`ParabolicSAR` output type.

    Args:
        value: `SAR` value.
        trend: Actual trend.
        ep: Extreme point.
        accel_factor: Acceleration factor.
    """

    value: float = None
    trend: SARTrend = None
    ep: float = None
    accel_factor: float = None


class ParabolicSAR(Indicator):
    """Parabolic Stop And Reverse.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [ParabolicSARVal][talipp.indicators.ParabolicSAR.ParabolicSARVal]

    Args:
        init_accel_factor: Initial acceleration factor.
        accel_factor_inc: Acceleration factor increment.
        max_accel_factor: Maximum acceleration factor.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    SAR_INIT_LEN = 5

    def __init__(self, init_accel_factor: float,
                 accel_factor_inc: float,
                 max_accel_factor: float,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=ParabolicSARVal,
                         input_sampling=input_sampling)

        self.init_accel_factor = init_accel_factor
        self.accel_factor_inc = accel_factor_inc
        self.max_accel_factor = max_accel_factor

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, ParabolicSAR.SAR_INIT_LEN):
            return None
        elif has_valid_values(self.input_values, ParabolicSAR.SAR_INIT_LEN, exact=True):
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
