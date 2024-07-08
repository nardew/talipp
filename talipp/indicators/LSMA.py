from dataclasses import dataclass
from typing import List, Any
import numpy as np

from talipp.indicator_util import has_valid_values
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.input import SamplingPeriodType, TimedValue, TimedValueExtractor


@dataclass
class LSMAVal:
    """`LSMA` output type.

    Args:
        slope: Slope of the least squares moving average regression.
        intercep: Intercept of the least squares moving average regression.
        pred: Predicted value.
    """

    slope: float = None
    intercept: float = None
    pred: float = None


class LSMA(Indicator):
    """Least Squares Moving Average.

    Input type: `float`

    Output type: [LSMAVal][talipp.indicators.LSMA.LSMAVal]

    Args:
        period: Period.
        input_values: List of input values.
        input_indicator: Input indicator.
        input_modifier: Input modifier.
        input_sampling: Input sampling type.
    """

    def __init__(
        self,
        period: int,
        input_values: List[TimedValue] = None,
        input_value_extractor=TimedValueExtractor,
        input_indicator: Indicator = None,
        input_modifier: InputModifierType = None,
        input_sampling: SamplingPeriodType = None,
    ):
        super().__init__(
            input_modifier=input_modifier,
            output_value_type=LSMAVal,
            input_sampling=input_sampling,
        )

        self.period = period
        self.v_get_timestamp = np.vectorize(input_value_extractor.get_timestamp)
        self.v_get_value = np.vectorize(input_value_extractor.get_value)

        #self.times = np.arange(
        #    start=0.0, stop=self.period, step=1.0, dtype=np.float64
        #)

        self.initialize(input_values, input_indicator)

    def _calculate_new_value(self) -> Any:
        if not has_valid_values(self.input_values, self.period):
            return None

        a_input_values = np.array(
            list(
                filter(
                    lambda v: isinstance(v, TimedValue),
                    self.input_values[-self.period :],
                )
            )
        )
        if len(a_input_values) == 0:
            return None

        times = self.v_get_timestamp(a_input_values)
        delta_t = (times[-1] - times[0]) / (self.period - 1)
        times = times - times[0]
        times = 1.0 + times / delta_t

        if np.count_nonzero(np.isnan(times)) == len(a_input_values):
            return None

        values = self.v_get_value(a_input_values)

        A = np.vstack([times, np.ones(len(times))]).T
        y = values[:, np.newaxis]
        pinv = np.linalg.pinv(A)
        alpha = pinv.dot(y)

        slope = alpha[0][0]
        intercept = alpha[1][0]

        pred = slope * self.period + intercept

        return LSMAVal(slope, intercept, pred)
