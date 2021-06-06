# =============================================================================
# Created By  : Pramit Biswas
# Created Date: Sun Jun 06 19:55:00 IST 2021
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

    def remove_input_value(self) -> None:
        for sub_indicator in self.sub_indicators:
            sub_indicator.remove_input_value()

        if len(self.input_values) > 0:
            value = self.input_values[-1]
            self.cumsumPV -= value.volume*(value.high+value.low+value.close)/3
            self.cumsumV -= value.volume
            self.input_values.pop(-1)

        self._remove_output_value()

        for lst in self.managed_sequences:
            if isinstance(lst, Indicator):
                lst.remove_input_value()
            else:
                if len(lst) > 0:
                    lst.pop(-1)

        self._remove_input_value_custom()

        for listener in self.output_listeners:
            listener.remove_input_value()
