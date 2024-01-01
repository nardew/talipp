from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ma import MAType, MAFactory


class TSI(Indicator):
    """
    True Strength Index

    Output: a list of floats
    """

    def __init__(self, fast_period: int, slow_period: int,
                 input_values: List[float] = None, input_indicator: Indicator = None, input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.EMA):
        super().__init__(input_modifier=input_modifier)

        self.slow_ma = MAFactory.get_ma(ma_type, slow_period)
        self.add_managed_sequence(self.slow_ma)
        self.fast_ma = MAFactory.get_ma(ma_type, fast_period, input_indicator = self.slow_ma)

        self.abs_slow_ma = MAFactory.get_ma(ma_type, slow_period)
        self.add_managed_sequence(self.abs_slow_ma)
        self.abs_fast_ma = MAFactory.get_ma(ma_type, fast_period, input_indicator = self.abs_slow_ma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        self.slow_ma.add(self.input_values[-1] - self.input_values[-2])
        self.abs_slow_ma.add(abs(self.input_values[-1] - self.input_values[-2]))

        if not has_valid_values(self.fast_ma, 1):
            return None

        if self.abs_fast_ma[-1] != 0:
            return 100.0 * (self.fast_ma[-1] / self.abs_fast_ma[-1])
        else:
            if has_valid_values(self.output_values, 1):
                return self.output_values[-1]
            else:
                return None
