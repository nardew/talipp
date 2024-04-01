from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.ATR import ATR
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


@dataclass
class VTXVal:
    """`VTX` output type.

    Args:
        plus_vtx: Positive movement.
        minus_vtx: Negative movement.
    """

    plus_vtx: float = None
    minus_vtx: float = None


class VTX(Indicator):
    """Vortex Indicator.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [VTXVal][talipp.indicators.VTX.VTXVal]

    Args:
        period: Period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=VTXVal,
                         input_sampling=input_sampling)

        self.period = period

        self.plus_vm = []
        self.add_managed_sequence(self.plus_vm)

        self.minus_vm = []
        self.add_managed_sequence(self.minus_vm)

        self.atr = ATR(1)
        self.add_sub_indicator(self.atr)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        value = self.input_values[-1]
        value2 = self.input_values[-2]

        self.plus_vm.append(abs(value.high - value2.low))
        self.minus_vm.append(abs(value.low - value2.high))

        if not has_valid_values(self.atr, self.period) or not has_valid_values(self.plus_vm, self.period) or \
                not has_valid_values(self.minus_vm, self.period):
            return None

        atr_sum = float(sum(self.atr[-self.period:]))
        return VTXVal(sum(self.plus_vm[-self.period:]) / atr_sum, sum(self.minus_vm[-self.period:]) / atr_sum)
