"""
Warning:
        The indicator is deprecated in favour of [ZigZag][talipp.indicators.ZigZag] indicator.
"""

import enum
from dataclasses import dataclass
from typing import List, Any

from talipp.exceptions import TalippException
from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class PivotType(enum.Enum):
    """Pivot type."""

    LOW = enum.auto()
    """Low pivot."""

    HIGH = enum.auto()
    """High pivot."""


@dataclass
class PivotsHLVal:
    """`PivotsHL` output type.

    Args:
        ohlcv: Pivot.
        type: Pivot type.
    """

    ohlcv: OHLCV = None
    type: PivotType = None


class PivotsHL(Indicator):
    """High/Low Pivots.

    Deprecated.

    Warning:
        Due to its nature the indicator does not support `update` and `remove` operations.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [PivotsHLVal][talipp.indicators.PivotsHL.PivotsHLVal]

    Important:
        Outputs of the indicator contain only pivots, i.e. length of the output does not match length of the input.

    Args:
        high_period: High pivot lookup period.
        low_period: Low pivot lookup period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, high_period: int,
                 low_period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=PivotsHLVal,
                         input_sampling=input_sampling)

        self.high_period = high_period
        self.low_period = low_period

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        # initialize the first pivot
        if has_valid_values(self.input_values, 1, exact=True):
            self.output_values.append(PivotsHLVal(self.input_values[-1], PivotType.LOW))
            return None

        ohlcv = self.input_values[-1]
        high = ohlcv.high
        low = ohlcv.low
        max_high = max(self.input_values[-self.high_period:], key=lambda x: x.high).high
        min_low = min(self.input_values[-self.low_period:], key=lambda x: x.low).low

        last_pivot: PivotsHLVal = self.output_values[-1]

        if high >= max_high:
            if last_pivot.type == PivotType.LOW:
                self.output_values.append(PivotsHLVal(self.input_values[-1], PivotType.HIGH))
            elif high >= last_pivot.ohlcv.high:
                self.output_values[-1] = PivotsHLVal(self.input_values[-1], PivotType.HIGH)
        elif low <= min_low:
            if last_pivot.type == PivotType.HIGH:
                self.output_values.append(PivotsHLVal(self.input_values[-1], PivotType.LOW))
            elif low <= last_pivot.ohlcv.low:
                self.output_values[-1] = PivotsHLVal(self.input_values[-1], PivotType.LOW)

        return None

    def update(self, value: Any) -> None:
        raise TalippException("Operation not supported.")

    def remove(self) -> None:
        raise TalippException("Operation not supported.")

    def purge_oldest(self, size: int) -> None:
        raise TalippException("Operation not supported.")

    # output_values are managed directly during the calculation
    def _add_to_output_values(self, value: Any) -> None:
        pass
