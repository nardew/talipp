from typing import List, Any

from talipp.indicators.Indicator import Indicator, ValueExtractorType
from talipp.ma import MAType, MAFactory


class DPO(Indicator):
    """
    Detrended Price Oscillator

    Output: a list of floats
    """

    def __init__(self, period: int, input_values: List[float] = None, input_indicator: Indicator = None,
                 value_extractor: ValueExtractorType = None, ma_type: MAType = MAType.SMA):
        super().__init__(value_extractor = value_extractor)

        self.period = period

        self.ma = MAFactory.get_ma(ma_type, period)
        self.add_sub_indicator(self.ma)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < int(self.period / 2) + 2 or len(self.ma) < 1:
            return None

        return self.input_values[-(int(self.period / 2) + 1) - 1] - float(self.ma[-1])
