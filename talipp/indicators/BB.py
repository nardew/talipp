from dataclasses import dataclass
from typing import List, Any

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.StdDev import StdDev
from talipp.input import SamplingPeriodType
from talipp.ma import MAType, MAFactory


@dataclass
class BBVal:
    """`BB` output type.

    Args:
        lb: Lower band.
        cb: Central band.
        ub: Upper band.
    """

    lb: float = None
    cb: float = None
    ub: float = None


class BB(Indicator):
    """Bollinger Bands.

    Input type: `float`

    Output type: [BBVal][talipp.indicators.BB.BBVal]

    Args:
        period: Period.
        std_dev_mult: Standard deviation multiplier.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(self, period: int,
                 std_dev_mult: float,
                 input_values: List[float] = None,
                 input_indicator: Indicator = None,
                 input_modifier: InputModifierType = None,
                 ma_type: MAType = MAType.SMA,
                 input_sampling: SamplingPeriodType = None):
        super().__init__(input_modifier=input_modifier,
                         output_value_type=BBVal,
                         input_sampling=input_sampling)

        self.period = period
        self.std_dev_mult = std_dev_mult

        self.central_band = MAFactory.get_ma(ma_type, period)
        self.std_dev = StdDev(self.period)

        self.add_sub_indicator(self.central_band)
        self.add_sub_indicator(self.std_dev)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        return BBVal(
            self.central_band[-1] - self.std_dev_mult * self.std_dev[-1],
            self.central_band[-1],
            self.central_band[-1] + self.std_dev_mult * self.std_dev[-1]
        )
