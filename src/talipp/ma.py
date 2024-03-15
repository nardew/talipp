from enum import Enum, auto
from typing import List

from talipp.indicators.DEMA import DEMA
from talipp.indicators.EMA import EMA
from talipp.indicators.HMA import HMA
from talipp.indicators.Indicator import Indicator, InputModifierType
from talipp.indicators.SMA import SMA
from talipp.indicators.SMMA import SMMA
from talipp.indicators.TEMA import TEMA
from talipp.indicators.VWMA import VWMA
from talipp.indicators.WMA import WMA


class MAType(Enum):
    ALMA = auto()
    SMA = auto()
    SMMA = auto()
    DEMA = auto()
    EMA = auto()
    HMA = auto()
    KAMA = auto()
    TEMA = auto()
    VWMA = auto()
    WMA = auto()


class MAFactory:
    @staticmethod
    def get_ma(ma_type: MAType,
               period: int,
               input_values: List[float] = None,
               input_indicator: Indicator = None,
               input_modifier: InputModifierType = None) -> Indicator:
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
        else:
            raise Exception(f"Unsupported moving average type {ma_type.name}.")
