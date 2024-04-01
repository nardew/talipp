from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values, previous_if_exists
from talipp.indicators.ATR import ATR
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


@dataclass
class ADXVal:
    """`ADX` output type.

    Args:
        adx: ADX.
        plus_di: Plus Directional Movement.
        minus_di: Minus Directional Movement.
    """

    adx: float = None
    plus_di: float = None
    minus_di: float = None


class ADX(Indicator):
    """Average Directional Index.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [ADXVal][talipp.indicators.ADX.ADXVal]

    Args:
        di_period: Directional Index period.
        adx_period: Average Directional Index period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, di_period: int,
                 adx_period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=ADXVal,
                         input_sampling=input_sampling)

        self.di_period = di_period
        self.adx_period = adx_period

        self.atr = ATR(di_period)
        self.add_sub_indicator(self.atr)

        # plus directional movement
        self.pdm = []
        # minus directional movement
        self.mdm = []

        self.add_managed_sequence(self.pdm)
        self.add_managed_sequence(self.mdm)

        # smoothed plus directional movement
        self.spdm = []
        # smoothed minus directional movement
        self.smdm = []

        self.add_managed_sequence(self.spdm)
        self.add_managed_sequence(self.smdm)

        # plus directional index
        self.pdi = []
        # minus directional index
        self.mdi = []

        self.add_managed_sequence(self.pdi)
        self.add_managed_sequence(self.mdi)

        # directional index
        self.dx = []
        self.add_managed_sequence(self.dx)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        current_input = self.input_values[-1]
        prev_input = self.input_values[-2]

        if current_input.high - prev_input.high > prev_input.low - current_input.low and current_input.high - prev_input.high > 0:
            self.pdm.append(current_input.high - prev_input.high)
        else:
            self.pdm.append(0)

        if prev_input.low - current_input.low > current_input.high - prev_input.high and prev_input.low - current_input.low > 0:
            self.mdm.append(prev_input.low - current_input.low)
        else:
            self.mdm.append(0)

        if not has_valid_values(self.pdm, self.di_period):
            return None
        elif has_valid_values(self.pdm, self.di_period, exact=True):
            self.spdm.append(sum(self.pdm[-self.di_period:]) / float(self.di_period))
            self.smdm.append(sum(self.mdm[-self.di_period:]) / float(self.di_period))
        elif len(self.pdm) > self.di_period:
            self.spdm.append((self.spdm[-1] * (self.di_period - 1) + self.pdm[-1]) / float(self.di_period))
            self.smdm.append((self.smdm[-1] * (self.di_period - 1) + self.mdm[-1]) / float(self.di_period))

        if self.atr[-1] != 0:
            self.pdi.append(100.0 * self.spdm[-1] / float(self.atr[-1]))
            self.mdi.append(100.0 * self.smdm[-1] / float(self.atr[-1]))
        else:
            self.pdi.append(previous_if_exists(self.pdi))
            self.mdi.append(previous_if_exists(self.mdi))

        dx_denom = (self.pdi[-1] + self.mdi[-1])
        if dx_denom != 0:
            self.dx.append(100.0 * float(abs(self.pdi[-1] - self.mdi[-1])) / dx_denom)
        else:
            self.dx.append(previous_if_exists(self.dx, default=0))

        adx = None
        if len(self.dx) == self.adx_period:
            adx = sum(self.dx) / float(self.adx_period)
        elif len(self.dx) > self.adx_period:
            adx = (self.output_values[-1].adx * (self.adx_period - 1) + self.dx[-1]) / float(self.adx_period)

        return ADXVal(adx, self.pdi[-1], self.mdi[-1])
