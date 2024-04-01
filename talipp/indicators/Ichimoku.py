from dataclasses import dataclass
from typing import List, Any

from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


@dataclass
class IchimokuVal:
    """`Ichimoku` output type.

    Args:
        base_line: Kijun Sen.
        conversion_line: Tenkan Sen.
        lagging_line: Chikou Span.
        cloud_leading_fast_line: Senkou Span.
        cloud_leading_slow_line: Senkou Span.
    """

    base_line: float = None
    conversion_line: float = None
    lagging_line: float = None
    cloud_leading_fast_line: float = None
    cloud_leading_slow_line: float = None


class Ichimoku(Indicator):
    """Ichimoku Cloud.

    Input type: [OHLCV][talipp.ohlcv.OHLCV]

    Output type: [IchimokuVal][talipp.indicators.Ichimoku.IchimokuVal]

    Args:
        kijun_period: Kijun (base line) period.
        tenkan_period: Tenkan (conversion line) period.
        chikou_lag_period: Chikou (lagging line) period.
        senkou_slow_period: Senkoun (leading) slow period.
        senkou_lookup_period: Senkoun (leading) fast period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """
    def __init__(self,
                 kijun_period: int,
                 tenkan_period: int,
                 chikou_lag_period: int,
                 senkou_slow_period: int,
                 senkou_lookup_period: int,
                 input_values: List[OHLCV] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=IchimokuVal,
                         input_sampling=input_sampling)

        self.kijun_period = kijun_period
        self.tenkan_period = tenkan_period
        self.chikou_lag_period = chikou_lag_period
        self.senkou_slow_period = senkou_slow_period
        self.senkou_lookup_period = senkou_lookup_period

        self.base_line = []         # Kijun Sen
        self.conversion_line = []   # Tenkan Sen
        self.lagging_line = []      # Chikou Span
        self.cloud_leading_fast_line = []   # Senkou Span
        self.cloud_leading_slow_line = []   # Senkou Span

        self.add_managed_sequence(self.base_line)
        self.add_managed_sequence(self.conversion_line)
        self.add_managed_sequence(self.lagging_line)
        self.add_managed_sequence(self.cloud_leading_fast_line)
        self.add_managed_sequence(self.cloud_leading_slow_line)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if len(self.input_values) >= self.kijun_period:
            max_high = max(self.input_values[-self.kijun_period:], key = lambda x: x.high).high
            min_low = min(self.input_values[-self.kijun_period:], key = lambda x: x.low).low

            self.base_line.append((max_high + min_low) / 2.0)

        if len(self.input_values) >= self.tenkan_period:
            max_high = max(self.input_values[-self.tenkan_period:], key = lambda x: x.high).high
            min_low = min(self.input_values[-self.tenkan_period:], key = lambda x: x.low).low

            self.conversion_line.append((max_high + min_low) / 2.0)

        if len(self.input_values) >= self.chikou_lag_period:
            self.lagging_line.append(self.input_values[-1].close)

        if len(self.base_line) >= self.senkou_lookup_period + 1 and len(self.conversion_line) >= self.senkou_lookup_period + 1:
            self.cloud_leading_fast_line.append((self.base_line[-self.senkou_lookup_period - 1] + self.conversion_line[-self.senkou_lookup_period - 1]) / 2.0)

        if len(self.input_values) >= self.senkou_slow_period + self.senkou_lookup_period + 1:
            max_high = max(self.input_values[-self.senkou_slow_period - self.senkou_lookup_period - 1:-self.senkou_lookup_period - 1], key = lambda x: x.high).high
            min_low = min(self.input_values[-self.senkou_slow_period - self.senkou_lookup_period - 1:-self.senkou_lookup_period - 1], key = lambda x: x.low).low

            self.cloud_leading_slow_line.append((max_high + min_low) / 2.0)

        return IchimokuVal(
            self.base_line[-1] if len(self.base_line) > 0 else None,
            self.conversion_line[-1] if len(self.conversion_line) > 0 else None,
            self.lagging_line[-1] if len(self.lagging_line) > 0 else None,
            self.cloud_leading_fast_line[-1] if len(self.cloud_leading_fast_line) > 0 else None,
            self.cloud_leading_slow_line[-1] if len(self.cloud_leading_slow_line) > 0 else None
        )
