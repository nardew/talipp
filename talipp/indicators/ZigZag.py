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
class ZigZagVal:
    """`ZigZag` output type.

    Args:
        ohlcv: Pivot.
        type: Pivot type.
    """

    ohlcv: OHLCV = None
    type: PivotType = None


class ZigZag(Indicator):
    """
    Warning:
        Due to its nature the indicator does not support `update` and `remove` operations.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [ZigZagVal][talipp.indicators.ZigZag.ZigZagVal]

    Important:
        Outputs of the indicator contain only pivots, i.e. length of the output does not match length of the input.

    Note:
        ZigZag indicator can also be used as a high/low pivots indicator if `sensitivity` is set to 0.

    Args:
        sensitivity: ZigZag sensitivity expressed as relative percentage change (e.g. 0.1 means change of 10%).
        min_trend_length: Minimum number of bars between two pivots.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    @dataclass
    class ZigZagValWrapper:
        zig_zag_val: ZigZagVal = None
        position: int = None

    def __init__(self, sensitivity: float,
                 min_trend_length: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=ZigZagVal,
                         input_sampling=input_sampling)

        self.sensitivity = sensitivity
        self.min_trend_length = min_trend_length

        self.last_pivot: ZigZag.ZigZagValWrapper = None

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        # initialize the first pivot
        if has_valid_values(self.input_values, 1, exact=True):
            self.output_values.append(ZigZagVal(self.input_values[-1], PivotType.LOW))
            self.last_pivot = ZigZag.ZigZagValWrapper(self.output_values[-1], len(self.input_values))
            return None

        ohlcv = self.input_values[-1]

        if self.last_pivot.zig_zag_val.type == PivotType.LOW:
            if ohlcv.high >= self.last_pivot.zig_zag_val.ohlcv.low * (1.0 + self.sensitivity) and self.trend_length_met():
                self.output_values.append(ZigZagVal(ohlcv, PivotType.HIGH))
                self.last_pivot = ZigZag.ZigZagValWrapper(self.output_values[-1], len(self.input_values))
            else:
                if ohlcv.low <= self.last_pivot.zig_zag_val.ohlcv.low:
                    self.output_values[-1] = ZigZagVal(ohlcv, PivotType.LOW)
                    self.last_pivot = ZigZag.ZigZagValWrapper(self.output_values[-1], len(self.input_values))
        else:
            if ohlcv.low <= self.last_pivot.zig_zag_val.ohlcv.high * (1.0 - self.sensitivity) and self.trend_length_met():
                self.output_values.append(ZigZagVal(ohlcv, PivotType.LOW))
                self.last_pivot = ZigZag.ZigZagValWrapper(self.output_values[-1], len(self.input_values))
            else:
                if ohlcv.high >= self.last_pivot.zig_zag_val.ohlcv.high:
                    self.output_values[-1] = ZigZagVal(ohlcv, PivotType.HIGH)
                    self.last_pivot = ZigZag.ZigZagValWrapper(self.output_values[-1], len(self.input_values))

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

    def trend_length_met(self):
        return len(self.input_values) - self.last_pivot.position >= self.min_trend_length
