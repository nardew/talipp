from collections.abc import Callable
from talipp.indicators.Smoother import SmoothedIndicator
from talipp.ma import MAFactory, MAType


class IndicatorFactory:
    """Indicator factory."""

    @staticmethod
    def get_smoother(indicator_class, ma_type: MAType = MAType.SMA):
        """
        Return a smoother indicator

        Args:
            indicator_class: indicator class
            smoothing_period: Smoothing period.
            ma_type: Moving average type.
        """
        return SmoothedIndicator(indicator_class, ma_type)
