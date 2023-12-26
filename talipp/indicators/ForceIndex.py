from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.indicators.EMA import EMA
from talipp.ohlcv import OHLCV
from talipp.ma import MAFactory, MAType


class ForceIndex(Indicator):
    """
    Force Index

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[OHLCV] = None, input_indicator: Indicator = None,
                 value_extractor: ValueExtractorType = None, ma_type: MAType = MAType.EMA):
        super().__init__(value_extractor = value_extractor)

        self.ma = MAFactory.get_ma(ma_type, period)
        self.add_managed_sequence(self.ma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        self.ma.add_input_value((self.input_values[-1].close - self.input_values[-2].close) * self.input_values[-1].volume)

        if len(self.ma) > 1:
            return self.ma[-1]
        else:
            return None
