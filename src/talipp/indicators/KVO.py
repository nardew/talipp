from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory
from talipp.ohlcv import OHLCV


class KVO(Indicator):
    """Klinger Volume Oscillator.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: `float`

    Args:
        fast_period: Fast moving average period.
        slow_period: Slow moving average period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
    """

    def __init__(self, fast_period: int,
                 slow_period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.EMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         input_sampling=input_sampling)

        self.fast_ma = MAFactory.get_ma(ma_type, fast_period)
        self.add_managed_sequence(self.fast_ma)

        self.slow_ma = MAFactory.get_ma(ma_type, slow_period)
        self.add_managed_sequence(self.slow_ma)

        self.trend = []
        self.add_managed_sequence(self.trend)

        self.cumulative_measurement = []
        self.add_managed_sequence(self.cumulative_measurement)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        value = self.input_values[-1]
        value2 = self.input_values[-2]

        if not has_valid_values(self.trend, 1):
            self.trend.append(0.0)
        else:
            if (value.high + value.low + value.close) > (value2.high + value2.low + value2.close):
                self.trend.append(1.0)
            else:
                self.trend.append(-1.0)

        if not has_valid_values(self.trend, 2):
            return None

        dm = value.high - value.low
        dm2 = value2.high - value2.low

        if not has_valid_values(self.cumulative_measurement, 1):
            prev_cm = dm
        else:
            prev_cm = self.cumulative_measurement[-1]

        if self.trend[-1] == self.trend[-2]:
            self.cumulative_measurement.append(prev_cm + dm)
        else:
            self.cumulative_measurement.append(dm2 + dm)

        if self.cumulative_measurement[-1] == 0:
            volume_force = 0.0
        else:
            volume_force = value.volume * abs(2 * (dm / self.cumulative_measurement[-1] - 1)) * self.trend[-1] * 100

        self.fast_ma.add(volume_force)
        self.slow_ma.add(volume_force)

        if not has_valid_values(self.fast_ma, 1) or not has_valid_values(self.slow_ma, 1):
            return None

        return self.fast_ma[-1] - self.slow_ma[-1]
