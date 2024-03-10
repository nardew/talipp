"""
The module contains functionality related to the processing of indicators' input.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum, auto

from talipp.ohlcv import OHLCV


class TimeUnitType(Enum):
    SEC = auto()
    MIN = auto()
    HOUR = auto()
    DAY = auto()


class SamplingPeriodType(Enum):
    """
    Available sampling periods.

    Each sampling period consists of a unit and its span. E.g. `SEC_1` means sampling every second, `SEC_3` means sampling every three seconds and so on.

    Note:
        Only those spans are allowed which divide full unit's period without remainder.

            3 seconds => OK (60 % 3 = 0)
            5 seconds => OK (60 % 5 = 0)
            8 seconds => NOT OK (60 % 8 != 0)
            4 hours   => OK (24 % 4 = 0)
            5 hours   => NOT OK (24 % 5 != 0)
    """

    SEC_1 = (TimeUnitType.SEC, 1)
    """1 second"""

    SEC_3 = (TimeUnitType.SEC, 3)
    """3 seconds"""

    SEC_5 = (TimeUnitType.SEC, 5)
    """5 seconds"""

    SEC_10 = (TimeUnitType.SEC, 10)
    """10 seconds"""

    SEC_15 = (TimeUnitType.SEC, 15)
    """15 seconds"""

    SEC_30 = (TimeUnitType.SEC, 30)
    """30 seconds"""

    MIN_1 = (TimeUnitType.MIN, 1)
    """1 minute"""

    MIN_3 = (TimeUnitType.MIN, 3)
    """3 minutes"""

    MIN_5 = (TimeUnitType.MIN, 5)
    """5 minutes"""

    MIN_10 = (TimeUnitType.MIN, 10)
    """10 minutes"""

    MIN_15 = (TimeUnitType.MIN, 15)
    """15 minutes"""

    MIN_30 = (TimeUnitType.MIN, 30)
    """30 minutes"""

    HOUR_1 = (TimeUnitType.HOUR, 1)
    """1 hour"""

    HOUR_2 = (TimeUnitType.HOUR, 2)
    """2 hours"""

    HOUR_3 = (TimeUnitType.HOUR, 3)
    """3 hours"""

    HOUR_4 = (TimeUnitType.HOUR, 4)
    """4 hours"""

    DAY_1 = (TimeUnitType.DAY, 1)
    """1 day"""
    
    
class Sampler:
    """Implementation of timeframe auto-sampling.

    Timeframe auto-sampling allows to evaluate whether two timestamps belong into the same [period][talipp.input.SamplingPeriodType] or not. This is later used by indicators to "merge" several input values received within selected timeframe and keep only the last value in the given timeframe.

    Each timeframe is counted from different starting point. Seconds are counted since whole minutes, minutes are counted since whole hours, hours are counted since whole days and days are counted since the beginning of the year.

    Examples:

        Sampling: 1 sec
        Timestamp 1: 00:00:01.000000
        Timestamp 2: 00:00:01.700000
        Result: same timeframe

        Sampling: 5 sec
        Timestamp 1: 00:00:01.000000
        Timestamp 2: 00:00:04.000000
        Result: same timeframe

        Sampling: 5 sec
        Timestamp 1: 00:00:04.000000
        Timestamp 2: 00:00:06.000000
        Result: different timeframe

    Args:
        period_type: The sampling period.
    """

    CONVERSION_TO_SEC = {
        TimeUnitType.SEC: 1,
        TimeUnitType.MIN: 60,
        TimeUnitType.HOUR: 3600,
        TimeUnitType.DAY: 3600 * 24,
    }

    def __init__(self, period_type: SamplingPeriodType):
        self._period_type: SamplingPeriodType = period_type

    def is_same_period(self, first: OHLCV, second: OHLCV) -> bool:
        """Evaluate whether two [OHLCV][talipp.ohlcv.OHLCV] objects belong to the same period.

        `OHLCV` objects have to contain time component to be comparable.

        Args:
            first: The first `OHLCV` object.
            second: The second `OHLCV` object.

        Returns:
            `True` if two objects belong to the same period, otherwise `False`.
        """

        first_normalized = self._normalize(first.time)
        second_normalized = self._normalize(second.time)

        return first_normalized == second_normalized

    def _normalize(self, dt: datetime):
        period_type = self._period_type.value[0]
        period_length = self._period_type.value[1]

        if period_type == TimeUnitType.SEC:
            period_start = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
        elif period_type == TimeUnitType.MIN:
            period_start = datetime(dt.year, dt.month, dt.day, dt.hour)
        elif period_type == TimeUnitType.HOUR:
            period_start = datetime(dt.year, dt.month, dt.day)
        elif period_type == TimeUnitType.DAY:
            period_start = datetime(dt.year, dt.month, 1)
        period_start = period_start.replace(tzinfo=dt.tzinfo)

        delta = dt - period_start
        num_periods = delta.total_seconds() // (period_length * Sampler.CONVERSION_TO_SEC[period_type])

        normalized_dt = period_start + timedelta(seconds=num_periods * period_length * Sampler.CONVERSION_TO_SEC[period_type])

        return normalized_dt
