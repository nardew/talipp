from talipp.indicators.OBV import OBV
from talipp.indicators.IndicatorFactory import IndicatorFactory
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
SOBV = IndicatorFactory.get_smoother(OBV, MAType.SMA)
