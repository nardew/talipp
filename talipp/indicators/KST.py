from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.ROC import ROC
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory


@dataclass
class KSTVal:
    """`KST` output type.

    Args:
        kst: `KST` value.
        signal: Signal line.
    """

    kst: float = None
    signal: float = None


class KST(Indicator):
    """Know Sure Thing.

    Input type: `float`

    Output type: [KSTVal][talipp.indicators.KST.KSTVal]

    Args:
        roc1_period: [ROC][talipp.indicators.ROC] period.
        roc1_ma_period: [ROC][talipp.indicators.ROC] moving average period.
        roc2_period: [ROC][talipp.indicators.ROC] period.
        roc2_ma_period: [ROC][talipp.indicators.ROC] moving average period.
        roc3_period: [ROC][talipp.indicators.ROC] period.
        roc3_ma_period: [ROC][talipp.indicators.ROC] moving average period.
        roc4_period: [ROC][talipp.indicators.ROC] period.
        roc4_ma_period: [ROC][talipp.indicators.ROC] moving average period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
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
                 input_values: List[float] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.SMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=KSTVal,
                         input_sampling=input_sampling)

        self.roc1 = ROC(roc1_period)
        self.roc2 = ROC(roc2_period)
        self.roc3 = ROC(roc3_period)
        self.roc4 = ROC(roc4_period)

        self.roc1_ma = MAFactory.get_ma(ma_type, roc1_ma_period, input_indicator=self.roc1)
        self.roc2_ma = MAFactory.get_ma(ma_type, roc2_ma_period, input_indicator=self.roc2)
        self.roc3_ma = MAFactory.get_ma(ma_type, roc3_ma_period, input_indicator=self.roc3)
        self.roc4_ma = MAFactory.get_ma(ma_type, roc4_ma_period, input_indicator=self.roc4)
        self.signal_line = MAFactory.get_ma(ma_type, signal_period)

        self.add_sub_indicator(self.roc1)
        self.add_sub_indicator(self.roc2)
        self.add_sub_indicator(self.roc3)
        self.add_sub_indicator(self.roc4)
        self.add_managed_sequence(self.signal_line)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if (not has_valid_values(self.roc1_ma, 1) or not has_valid_values(self.roc2_ma, 1) or
                not has_valid_values(self.roc3_ma, 1) or not has_valid_values(self.roc4_ma, 1)):
            return None

        kst = 1.0 * self.roc1_ma[-1] + 2.0 * self.roc2_ma[-1] + 3.0 * self.roc3_ma[-1] + 4.0 * self.roc4_ma[-1]
        self.signal_line.add(kst)

        if has_valid_values(self.signal_line):
            signal_value = self.signal_line[-1]
        else:
            signal_value = None

        return KSTVal(kst, signal_value)
