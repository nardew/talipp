from dataclasses import dataclass
from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.indicators.SMA import SMA
from talipp.indicators.StdDev import StdDev


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

    def __init__(self, period: int, std_dev_multiplier: float, input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.period = period
        self.std_dev_multiplier = std_dev_multiplier

        self.central_band = SMA(self.period)
        self.std_dev = StdDev(self.period)

        self.add_sub_indicator(self.central_band)
        self.add_sub_indicator(self.std_dev)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < self.period:
            return None
        else:
            return BBVal(
                self.central_band[-1] - self.std_dev_multiplier * self.std_dev[-1],
                self.central_band[-1],
                self.central_band[-1] + self.std_dev_multiplier * self.std_dev[-1]
            )
