from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.ma import MAFactory, MAType
from talipp.ohlcv import OHLCV


class ForceIndex(Indicator):
    """
    Force Index

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None, ma_type: MAType = MAType.EMA):
        super().__init__(input_modifier=input_modifier)

        self.ma = MAFactory.get_ma(ma_type, period)
        self.add_managed_sequence(self.ma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        self.ma.add((self.input_values[-1].close - self.input_values[-2].close) * self.input_values[-1].volume)

        if not has_valid_values(self.ma, 1):
            return None

        return self.ma[-1]
