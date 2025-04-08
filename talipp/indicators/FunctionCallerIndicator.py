from typing import Any
from collections.abc import Callable
from talipp.indicators.Indicator import Indicator


class FunctionCallerIndicator(Indicator):
    def __init__(self, func: Callable):
        super().__init__()

        self._func = func

    def __call__(
        self,
        input_values=None,
        input_indicator=None,
        *args: Any,
        **kwargs
    ) -> Any:
        self.initialize(input_values, input_indicator)
        return self

    def _calculate_new_value(self) -> Any:
        return self._func(self.input_values[-1])
