import enum
from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.ohlcv import OHLCV


class HLType(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


@dataclass
class PivotsHLVal:
    ohlcv: OHLCV = None
    type: HLType = None


class PivotsHL(Indicator):
    """
    High/Low Pivots

    Output: a list of PivotsHLVal
    """

    def __init__(self, high_period: int, low_period: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.high_period = high_period
        self.low_period = low_period

        self.initialize(input_values)

    # Always return None to avoid automatic update of output_results. They are handled in the method manually
    # The indicator always works with the last but one input value because it cannot handle updates/removals properly.
    # Furthermore, the indicator does not support removing two values in a row
    def _calculate_new_value(self) -> Any:
        if len(self.input_values) < 2:
            return None

        high = self.input_values[-2].high
        low = self.input_values[-2].low
        max_high = max(self.input_values[-self.high_period:], key=lambda x: x.high).high
        min_low = min(self.input_values[-self.low_period:], key=lambda x: x.low).low

        if high >= max_high:
            if len(self.output_values) == 0 or self.output_values[-1].type == HLType.LOW:
                self.output_values.append(PivotsHLVal(self.input_values[-2], HLType.HIGH))
            elif high >= self.output_values[-1].ohlcv.high:
                self.output_values[-1] = PivotsHLVal(self.input_values[-2], HLType.HIGH)
        elif low <= min_low:
            if len(self.output_values) == 0 or self.output_values[-1].type == HLType.HIGH:
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
