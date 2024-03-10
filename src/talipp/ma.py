"""Utilities for moving averages."""

from enum import Enum, auto
from typing import List

from talipp.exceptions import TalippException
from talipp.indicators.DEMA import DEMA
from talipp.indicators.EMA import EMA
from talipp.indicators.HMA import HMA
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.SMA import SMA
from talipp.indicators.SMMA import SMMA
from talipp.indicators.T3 import T3
from talipp.indicators.TEMA import TEMA
from talipp.indicators.TRIX import TRIX
from talipp.indicators.VWMA import VWMA
from talipp.indicators.WMA import WMA
from talipp.indicators.ZLEMA import ZLEMA


class MAType(Enum):
    """Moving average type enum."""

    ALMA = auto()
    """[Arnaud Legoux Moving Average][talipp.indicators.ALMA]"""

    DEMA = auto()
    """[Double Exponential Moving Average][talipp.indicators.DEMA]"""

    EMA = auto()
    """[Exponential Moving Average][talipp.indicators.EMA]"""

    HMA = auto()
    "[Hull Moving Average][talipp.indicators.HMA]"

    KAMA = auto()
    """[Kaufman's Adaptive Moving Average][talipp.indicators.KAMA]"""

    SMA = auto()
    """[Standard Moving Average][talipp.indicators.SMA]"""

    SMMA = auto()
    """[Smoothed Moving Average][talipp.indicators.SMMA]"""

    T3 = auto()
    """[T3 Moving Average][talipp.indicators.T3]"""

    TEMA = auto()
    """[Triple Exponential Moving Average][talipp.indicators.TEMA]"""

    TRIX = auto()
    """[TRIX][talipp.indicators.TRIX]"""

    VWMA = auto()
    """[Volume Weighted Moving Average][talipp.indicators.VWMA]"""

    WMA = auto()
    """[Weighted Moving Average][talipp.indicators.WMA]"""

    ZLEMA = auto()
    """[Zero Lag Exponential Moving Average][talipp.indicators.ZLEMA]"""


class MAFactory:
    """Moving average object factory."""

    @staticmethod
    def get_ma(ma_type: MAType,
               period: int,
               input_values: List[float] = None,
               input_indicator: Indicator = None,
               input_modifier: InputModifierType = None) -> Indicator:
        """Return a moving average indicator for given [moving average type][talipp.ma.MAType].

            Only moving averages which do not have other than `period` parameter can be generated (unless they provide default values for them).

            Args:
                ma_type: The moving average to be generated.
                period: The period to be passed into the moving average object.
                input_values: The input values to be passed into the moving average object.
                input_indicator: The input indicator to be passed into the moving average object.
                input_modifier: The input modifier to be passed into the moving average object.

            Returns:
                Moving average indicator.

            Raises:
                TalippException: Unsupported moving average type passed in.
            """
        if ma_type == MAType.SMA:
            return SMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.SMMA:
            return SMMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.DEMA:
            return DEMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.EMA:
            return EMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.TEMA:
            return TEMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.HMA:
            return HMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.VWMA:
            return VWMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.WMA:
            return WMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.T3:
            return T3(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.TRIX:
            return TRIX(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        elif ma_type == MAType.ZLEMA:
            return ZLEMA(period=period, input_values=input_values, input_indicator=input_indicator, input_modifier=input_modifier)
        else:
            raise TalippException(f"Unsupported moving average type {ma_type.name}.")
