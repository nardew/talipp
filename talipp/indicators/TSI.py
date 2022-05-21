from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.EMA import EMA


class TSI(Indicator):
    """
    True Strength Index

    Output: a list of floats
    """

    def __init__(self, fast_period: int, slow_period: int,
                 input_values: List[float] = None, input_indicator: Indicator = None, value_extractor: ValueExtractorType = None):
        super().__init__(value_extractor = value_extractor)

        self.slow_ema = EMA(slow_period)
        self.add_managed_sequence(self.slow_ema)
        self.fast_ema = EMA(fast_period, input_indicator = self.slow_ema)

        self.abs_slow_ema = EMA(slow_period)
        self.add_managed_sequence(self.abs_slow_ema)
        self.abs_fast_ema = EMA(fast_period, input_indicator = self.abs_slow_ema)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        self.slow_ema.add_input_value(self.input_values[-1] - self.input_values[-2])
        self.abs_slow_ema.add_input_value(abs(self.input_values[-1] - self.input_values[-2]))

        if len(self.fast_ema) < 1:
            return None

        if self.abs_fast_ema[-1] != 0:
            return 100.0 * (self.fast_ema[-1] / self.abs_fast_ema[-1])
        else:
            if len(self.output_values) > 0:
                return self.output_values[-1]
            else:
                return None