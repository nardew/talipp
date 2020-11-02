from typing import List, Any

from talipp.indicators.Indicator import Indicator


class KAMA(Indicator):
    """
    Kaufman's Adaptive Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, fast_ema_constant_period: int, slow_ema_constant_period: int,
                 input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period

        self.fast_smoothing_constant = 2.0 / (fast_ema_constant_period + 1)
        self.slow_smoothing_constant = 2.0 / (slow_ema_constant_period + 1)

        self.volatilities = []
        self.add_managed_sequence(self.volatilities)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        self.volatilities.append(abs(self.input_values[-1] - self.input_values[-2]))

        if len(self.volatilities) < self.period:
            return None

        volatility = sum(self.volatilities[-self.period:])
        change = abs(self.input_values[-1] - self.input_values[-self.period - 1])

        if volatility != 0:
            efficiency_ratio = float(change) / volatility
        else:
            efficiency_ratio = 0

        smoothing_constant = (efficiency_ratio * (self.fast_smoothing_constant - self.slow_smoothing_constant) + self.slow_smoothing_constant)**2

        if len(self.output_values) == 0:
            prev_kama = self.input_values[-2]
        else:
            prev_kama = self.output_values[-1]

        return prev_kama + smoothing_constant * (self.input_values[-1] - prev_kama)

