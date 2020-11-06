from typing import List, Any

from talipp.indicators.Indicator import Indicator
from math import exp


class ALMA(Indicator):
    """
    Arnaud Legoux Moving Average

    Output: a list of floats
    """

    def __init__(self, period: int, offset: float, sigma: float, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period
        self.offset = offset
        self.sigma = sigma

        # calculate weights and normalisation factor (w_sum)
        self.w = []
        self.w_sum = 0.0
        s = self.period / float(self.sigma)
        m = int((self.period - 1) * self.offset)
        for i in range(0, self.period):
            self.w.append(exp(-1 * (i - m) * (i - m) / (2 * s * s)))
            self.w_sum += self.w[-1]

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None
        else:
            alma = 0.0
            for i in range(0, self.period):
                alma += self.input_values[-(self.period - i)] * self.w[i]

            return alma / self.w_sum
