from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.indicators.ATR import ATR
from talipp.ohlcv import OHLCV


@dataclass
class ADXVal:
    adx: float = None
    plus_di: float = None
    minus_di: float = None


class ADX(Indicator):
    """
    Average Directional Index

    Output: a list of ADXVal
    """
    def __init__(self, period_di: int, period_adx: int, input_values: List[OHLCV] = None):
        super(ADX, self).__init__()

        self.period_di = period_di
        self.period_adx = period_adx

        self.atr = ATR(period_di)
        self.add_sub_indicator(self.atr)

        # plus directional movement
        self.pdm = []
        # minus directional movement
        self.mdm = []

        self.add_managed_sequence(self.pdm)
        self.add_managed_sequence(self.mdm)

        # smoothed plus directional movement
        self.spdm = []
        # smoothed minus directional movement
        self.smdm = []

        self.add_managed_sequence(self.spdm)
        self.add_managed_sequence(self.smdm)

        # plus directional index
        self.pdi = []
        # minus directional index
        self.mdi = []

        self.add_managed_sequence(self.pdi)
        self.add_managed_sequence(self.mdi)

        # directional index
        self.dx = []
        self.add_managed_sequence(self.dx)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        current_input = self.input_values[-1]
        prev_input = self.input_values[-2]

        if current_input.high - prev_input.high > prev_input.low - current_input.low and current_input.high - prev_input.high > 0:
            self.pdm.append(current_input.high - prev_input.high)
        else:
            self.pdm.append(0)

        if prev_input.low - current_input.low > current_input.high - prev_input.high and prev_input.low - current_input.low > 0:
            self.mdm.append(prev_input.low - current_input.low)
        else:
            self.mdm.append(0)

        if len(self.pdm) < self.period_di:
            return None
        elif len(self.pdm) == self.period_di:
            self.spdm.append(sum(self.pdm[-self.period_di:]) / float(self.period_di))
            self.smdm.append(sum(self.mdm[-self.period_di:]) / float(self.period_di))
        elif len(self.pdm) > self.period_di:
            self.spdm.append((self.spdm[-1] * (self.period_di - 1) + self.pdm[-1]) / float(self.period_di))
            self.smdm.append((self.smdm[-1] * (self.period_di - 1) + self.mdm[-1]) / float(self.period_di))

        self.pdi.append(100.0 * self.spdm[-1] / float(self.atr[-1]))
        self.mdi.append(100.0 * self.smdm[-1] / float(self.atr[-1]))

        self.dx.append(100.0 * float(abs(self.pdi[-1] - self.mdi[-1])) / (self.pdi[-1] + self.mdi[-1]))

        adx = None
        if len(self.dx) == self.period_adx:
            adx = sum(self.dx) / float(self.period_adx)
        elif len(self.dx) > self.period_adx:
            adx = (self.output_values[-1].adx * (self.period_adx - 1) + self.dx[-1]) / float(self.period_adx)

        return ADXVal(adx, self.pdi[-1], self.mdi[-1])
