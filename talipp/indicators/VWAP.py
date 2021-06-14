# =============================================================================
# Created By   : Pramit Biswas
# Creation Date: Sun Jun 06 19:55:00 IST 2021
# =============================================================================

from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class VWAP(Indicator):
    """
    Volume Weighted Average Price
    Output: a list of floats
    ALERT: This does not check season starting.
    """

    def __init__(self, input_values: List[OHLCV] = None):
        super().__init__()

        self.cumsumPV = []
        self.cumsumV = []

        self.add_managed_sequence(self.cumsumPV)
        self.add_managed_sequence(self.cumsumV)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]

        if self.cumsumPV:
            self.cumsumPV.append(self.cumsumPV[-1]
                                 + value.volume*(value.high
                                                 + value.low + value.close)/3)
            self.cumsumV.append(self.cumsumV[-1] + value.volume)
        else:
            self.cumsumPV.append(value.volume*(value.high
                                               + value.low + value.close)/3)
            self.cumsumV.append(value.volume)

        if (self.cumsumV[-1] != 0):
            return self.cumsumPV[-1]/self.cumsumV[-1]
        else:
            return None
