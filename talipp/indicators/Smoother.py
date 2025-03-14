from typing import Any
from talipp.indicators.Indicator import Indicator
from talipp.ma import MAFactory, MAType


class Smoother(Indicator):
    def __init__(self, indicator_class, ma_type: MAType):
        super().__init__()

        self.indicator_class = indicator_class
        self.ma_type = ma_type

    def __call__(
        self,
        smoothing_period: int,
        input_values=None,
        input_indicator=None,
        *args: Any,
        **kwargs
    ) -> Any:
        self.ma = MAFactory.get_ma(self.ma_type, smoothing_period)

        self.internal_indicator = self.indicator_class(*args, **kwargs)
        self.add_sub_indicator(self.internal_indicator)

        self.initialize(input_values, input_indicator)

        return self

    def _calculate_new_value(self) -> Any:
        self.ma.add(self.internal_indicator.output_values)
        return self.ma.output_values[-1]
