from collections.abc import Callable
from talipp.indicators.FunctionCallerIndicator import FunctionCallerIndicator


class IndicatorFactory:
    """Indicator factory."""

    @staticmethod
    def get_function_caller(func: Callable):
        """
        Return a function caller indicator
        Args:
            func: Function which is called when input occurs.
        """
        return FunctionCallerIndicator(func)
