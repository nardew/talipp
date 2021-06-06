from typing import List, Any

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV

import numpy as np


class VWAP(Indicator):
    """
    Volume Weight Average Price
    Output: a list of floats
    ALERT: This does not check season start.
    """

    def __init__(self, input_values: List[OHLCV] = None):
        super().__init__()

        self.cumsumPV = 0
        self.cumsumV = 0
        
        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        value = self.input_values[-1]
        
        self.cumsumPV += value.volume*(value.high+value.low+value.close)/3
        self.cumsumV += value.volume

        if (self.cumsumV != 0):
            return self.cumsumPV/self.cumsumV
        else:
            return None