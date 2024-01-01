from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.StdDev import StdDev
from talipp.ma import MAType, MAFactory


@dataclass
class BBVal:
    # lower band
    lb: float = None

    # central band
    cb: float = None

    # upper band
    ub: float = None


class BB(Indicator):
    """
    Bollinger Bands

    Output: a list of BBVal
    """

    def __init__(self, period: int, std_dev_mult: float, input_values: List[float] = None,
                 input_indicator: Indicator = None, input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.SMA):
        super().__init__(input_modifier=input_modifier, output_value_type=BBVal)

        self.period = period
        self.std_dev_mult = std_dev_mult

        self.central_band = MAFactory.get_ma(ma_type, period, input_modifier=input_modifier)
        self.std_dev = StdDev(self.period, input_modifier=input_modifier)

        self.add_sub_indicator(self.central_band)
        self.add_sub_indicator(self.std_dev)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        return BBVal(
            self.central_band[-1] - self.std_dev_mult * self.std_dev[-1],
            self.central_band[-1],
            self.central_band[-1] + self.std_dev_mult * self.std_dev[-1]
        )
