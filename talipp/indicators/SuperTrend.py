import enum
from typing import List, Any
from dataclasses import dataclass

from talipp.indicators.Indicator import Indicator
from talipp.indicators.ATR import ATR
from talipp.ohlcv import OHLCV


class Trend(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()


@dataclass
class SuperTrendVal:
    value: float = None
    trend: Trend = None


class SuperTrend(Indicator):
    """
    Output: A list of SuperTrendVal
    """

    def __init__(self, atr_period: int, mult: int, input_values: List[OHLCV] = None):
        super().__init__()

        self.atr = ATR(atr_period)
        self.mult = mult

        # final upper band
        self.fub = []
        # final lower band
        self.flb = []

        self.add_sub_indicator(self.atr)
        self.add_managed_sequence(self.fub)
        self.add_managed_sequence(self.flb)

        self.initialize(input_values)

    def _calculate_new_value(self) -> Any:
        if len(self.atr) == 0:
            return None

        """
        BASIC UPPER BAND = HLA + [ MULTIPLIER * 10-DAY ATR ]
        BASIC LOWER BAND = HLA - [ MULTIPLIER * 10-DAY ATR ]
        """

        hla = (self.input_values[-1].high + self.input_values[-1].low) / 2.0
        bub = hla + self.mult * self.atr[-1]
        blb = hla - self.mult * self.atr[-1]

        """
        IF C.BUB < P.FUB OR P.CLOSE > P.FUB: C.FUB = C.BUB
        IF THE CONDITION IS NOT SATISFIED: C.FUB = P.FUB
        """

        if len(self.fub) == 0:
            fub = 0
        elif bub < self.fub[-1] or self.input_values[-2].close > self.fub[-1]:
            fub = bub
        else:
            fub = self.fub[-1]
        self.fub.append(fub)

        """
        IF C.BLB > P.FLB OR P.CLOSE < P.FLB: C.FLB = C.BLB
        IF THE CONDITION IS NOT SATISFIED: C.FLB = P.FLB
        """

        if len(self.flb) == 0:
            flb = 0
        elif blb > self.flb[-1] or self.input_values[-2].close < self.flb[-1]:
            flb = blb
        else:
            flb = self.flb[-1]
        self.flb.append(flb)

        """
        IF P.ST == P.FUB AND C.CLOSE < C.FUB: C.ST = C.FUB
        IF P.ST == P.FUB AND C.CLOSE > C.FUB: C.ST = C.FLB
        IF P.ST == P.FLB AND C.CLOSE > C.FLB: C.ST = C.FLB
        IF P.ST == P.FLB AND C.CLOSE < C.FLB: C.ST = C.FUB
        """

        if len(self.output_values) == 0:
            supertrend = 0
        elif (self.output_values[-1].value == self.fub[-2] and self.input_values[-1].close <= self.fub[-1]):
            supertrend = self.fub[-1]
        elif self.output_values[-1].value == self.fub[-2] and self.input_values[-1].close > self.fub[-1]:
            supertrend = self.flb[-1]
        elif self.output_values[-1].value == self.flb[-2] and self.input_values[-1].close >= self.flb[-1]:
            supertrend = self.flb[-1]
        elif self.output_values[-1].value == self.flb[-2] and self.input_values[-1].close < self.flb[-1]:
            supertrend = self.fub[-1]

        return SuperTrendVal(supertrend, Trend.UP if self.input_values[-1].close > supertrend else Trend.DOWN)
