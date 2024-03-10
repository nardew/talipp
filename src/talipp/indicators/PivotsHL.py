import enum
from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class HLType(enum.Enum):
    """Pivot type."""

    LOW = enum.auto()
    """Low pivot."""

    HIGH = enum.auto()
    """High pivot."""


@dataclass
class PivotsHLVal:
    """`ParabolicSAR` output type.

    Args:
        ohlcv: Pivot.
        type: Pivot type.
    """

    ohlcv: OHLCV = None
    type: HLType = None


class PivotsHL(Indicator):
    """High/Low Pivots.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [PivotsHLVal][talipp.indicators.PivotsHL.PivotsHLVal]

    Args:
        high_period: High pivot lookup period.
        low_period: Low pivot lookup period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.

    Warning:
        The indicator always works with the last but one input value because it cannot handle updates/removals properly. Furthermore, the indicator does not support removing two values in a row.
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

    # Always return None to avoid automatic update of output_results. They are handled in the method manually.
    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, 2):
            return None

        high = self.input_values[-2].high
        low = self.input_values[-2].low
        max_high = max(self.input_values[-self.high_period:], key=lambda x: x.high).high
        min_low = min(self.input_values[-self.low_period:], key=lambda x: x.low).low

        if high >= max_high:
            if not has_valid_values(self.output_values, 1) or self.output_values[-1].type == HLType.LOW:
                self.output_values.append(PivotsHLVal(self.input_values[-2], HLType.HIGH))
            elif high >= self.output_values[-1].ohlcv.high:
                self.output_values[-1] = PivotsHLVal(self.input_values[-2], HLType.HIGH)
        elif low <= min_low:
            if not has_valid_values(self.output_values, 1) or self.output_values[-1].type == HLType.HIGH:
                self.output_values.append(PivotsHLVal(self.input_values[-2], HLType.LOW))
            elif low <= self.output_values[-1].ohlcv.low:
                self.output_values[-1] = PivotsHLVal(self.input_values[-2], HLType.LOW)

        return None

    # override the method to avoid automatic cleanup of output_results
    def _remove_output_value(self) -> None:
        pass

    # override the method to avoid automatic cleanup of output_results
    def _purge_oldest_output_value(self, size: int) -> None:
        pass

    # override the method to avoid automatic update of output_results
    def _add_to_output_values(self, value: Any) -> None:
        pass
