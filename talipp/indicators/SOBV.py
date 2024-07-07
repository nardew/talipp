from talipp.indicators.OBV import OBV
from talipp.indicators.Smoother import SmootherFactory
from talipp.ma import MAType


"""Smoothed On Balance Volume.
Input type: [OHLCV][talipp.ohlcv.OHLCV]
Output type: `float`
Args:
    period: Moving average period.
    input_values: List of input values.
    input_indicator: Input indicator.
    input_modifier: Input modifier.
    input_sampling: Input sampling type.
"""
SOBV = SmootherFactory.get_smoother(OBV, MAType.SMA)
