from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.indicators.SMA import SMA
from talipp.indicators.ROC import ROC


@dataclass
class KSTVal:
    kst: float = None
    signal: float = None


class KST(Indicator):
    """
    Know Sure Thing

    Output: a list of KSTVal
    """

    def __init__(self,
                 roc1_period: int,
                 roc1_ma_period: int,
                 roc2_period: int,
                 roc2_ma_period: int,
                 roc3_period: int,
                 roc3_ma_period: int,
                 roc4_period: int,
                 roc4_ma_period: int,
                 signal_period: int,
                 input_values: List[float] = None, input_indicator: Indicator = None):
        super().__init__()

        self.roc1 = ROC(roc1_period)
        self.roc2 = ROC(roc2_period)
        self.roc3 = ROC(roc3_period)
        self.roc4 = ROC(roc4_period)

        self.roc1_ma = SMA(roc1_ma_period)
        self.roc2_ma = SMA(roc2_ma_period)
        self.roc3_ma = SMA(roc3_ma_period)
        self.roc4_ma = SMA(roc4_ma_period)
        self.signal_line = SMA(signal_period)

        self.add_sub_indicator(self.roc1)
        self.add_sub_indicator(self.roc2)
        self.add_sub_indicator(self.roc3)
        self.add_sub_indicator(self.roc4)

        self.add_managed_sequence(self.roc1_ma)
        self.add_managed_sequence(self.roc2_ma)
        self.add_managed_sequence(self.roc3_ma)
        self.add_managed_sequence(self.roc4_ma)
        self.add_managed_sequence(self.signal_line)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if self.roc1.has_output_value():
            self.roc1_ma.add_input_value(self.roc1[-1])
        if self.roc2.has_output_value():
            self.roc2_ma.add_input_value(self.roc2[-1])
        if self.roc3.has_output_value():
            self.roc3_ma.add_input_value(self.roc3[-1])
        if self.roc4.has_output_value():
            self.roc4_ma.add_input_value(self.roc4[-1])

        if not self.roc1_ma.has_output_value() or not self.roc2_ma.has_output_value() or not self.roc3_ma.has_output_value() or not self.roc4_ma.has_output_value():
            return None

        kst = 1.0 * self.roc1_ma[-1] + 2.0 * self.roc2_ma[-1] + 3.0 * self.roc3_ma[-1] + 4.0 * self.roc4_ma[-1]
        self.signal_line.add_input_value(kst)

        if len(self.signal_line) > 0:
            signal_value = self.signal_line[-1]
        else:
            signal_value = None

        return KSTVal(kst, signal_value)
