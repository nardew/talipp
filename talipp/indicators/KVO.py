from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.EMA import EMA
from talipp.ohlcv import OHLCV


class KVO(Indicator):
    """
    Klinger Volume Oscillator

    Output: a list of floats
    """

    def __init__(self, fast_period: int, slow_period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.fast_ema = EMA(fast_period)
        self.add_managed_sequence(self.fast_ema)

        self.slow_ema = EMA(slow_period)
        self.add_managed_sequence(self.slow_ema)

        self.trend = []
        self.add_managed_sequence(self.trend)

        self.cumulative_measurement = []
        self.add_managed_sequence(self.cumulative_measurement)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        value = self.input_values[-1]
        value2 = self.input_values[-2]

        if len(self.trend) < 1:
            self.trend.append(0.0)
        else:
            if (value.high + value.low + value.close) > (value2.high + value2.low + value2.close):
                self.trend.append(1.0)
            else:
                self.trend.append(-1.0)

        if len(self.trend) < 2:
            return None

        dm = value.high - value.low
        dm2 = value2.high - value2.low

        if len(self.cumulative_measurement) < 1:
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

        self.fast_ema.add_input_value(volume_force)
        self.slow_ema.add_input_value(volume_force)

        if len(self.fast_ema) < 1 or len(self.slow_ema) < 1:
            return None

        #print(f"kvo: {self.fast_ema[-1] - self.slow_ema[-1]} vf: {volume_force} dm: {dm} cm: {self.cumulative_measurement[-1]} trend: {self.trend[-1]} volume: {value.volume}")

        return self.fast_ema[-1] - self.slow_ema[-1]