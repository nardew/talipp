from talipp.indicators.Smoother import Smoother
from talipp.ma import MAType


class IndicatorFactory:
    """Indicator factory."""

    @staticmethod
    def get_smoother(indicator_class, ma_type: MAType = MAType.SMA):
        """
        Return a smoother ie an indicator which can smoothed input values using a moving average

        Args:
            indicator_class: indicator class
            ma_type: Moving average type.
        """
        return Smoother(indicator_class, ma_type)
