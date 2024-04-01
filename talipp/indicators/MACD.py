from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory


@dataclass
class MACDVal:
    """`MACD` output type.

    Args:
        macd: `MACD` value.
        signal: Signal line.
        histogram: Histogram.
    """

    macd: float = None
    signal: float = None
    histogram: float = None


class MACD(Indicator):
    """Moving Average Convergence Divergence.

    Input type: `float`

    Output type: [MACDVal][talipp.indicators.MACD.MACDVal]

    Args:
        fast_period: Fast moving average period.
        slow_period: Slow moving average period.
        signal_period: Signal line moving average period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        ma_type: Moving average type.
        input_sampling: Input sampling type.
    """

    def __init__(self, fast_period: int,
                 slow_period: int,
                 signal_period: int,
                 input_values: List[float] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.EMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=MACDVal,
                         input_sampling=input_sampling)

        self.ma_fast = MAFactory.get_ma(ma_type, fast_period)
        self.ma_slow = MAFactory.get_ma(ma_type, slow_period)
        self.signal_line = MAFactory.get_ma(ma_type, signal_period)

        self.add_sub_indicator(self.ma_fast)
        self.add_sub_indicator(self.ma_slow)
        self.add_managed_sequence(self.signal_line)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.ma_fast, 1) or not has_valid_values(self.ma_slow, 1):
            return None

        macd = self.ma_fast[-1] - self.ma_slow[-1]
        self.signal_line.add(macd)

        if has_valid_values(self.signal_line, 1):
            signal = self.signal_line[-1]
        else:
            signal = None

        histogram = None
        if macd is not None and signal is not None:
            histogram = macd - signal

        return MACDVal(macd, signal, histogram)
