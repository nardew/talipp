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
    SEC_1 = (TimeUnitType.SEC, 1)
    SEC_3 = (TimeUnitType.SEC, 3)
    SEC_5 = (TimeUnitType.SEC, 5)
    SEC_10 = (TimeUnitType.SEC, 10)
    SEC_15 = (TimeUnitType.SEC, 15)
    SEC_30 = (TimeUnitType.SEC, 30)
    MIN_1 = (TimeUnitType.MIN, 1)
    MIN_3 = (TimeUnitType.MIN, 3)
    MIN_5 = (TimeUnitType.MIN, 5)
    MIN_10 = (TimeUnitType.MIN, 10)
    MIN_15 = (TimeUnitType.MIN, 15)
    MIN_30 = (TimeUnitType.MIN, 30)
    HOUR_1 = (TimeUnitType.HOUR, 1)
    HOUR_2 = (TimeUnitType.HOUR, 2)
    HOUR_3 = (TimeUnitType.HOUR, 3)
    HOUR_4 = (TimeUnitType.HOUR, 4)
    DAY_1 = (TimeUnitType.DAY, 1)
    
    
class Sampler:
    CONVERSION_TO_SEC = {
        TimeUnitType.SEC: 1,
        TimeUnitType.MIN: 60,
        TimeUnitType.HOUR: 3600,
        TimeUnitType.DAY: 3600 * 24,
    }

    def __init__(self, period_type: SamplingPeriodType):
        self.period_type: SamplingPeriodType = period_type

    def is_same_period(self, current_value: OHLCV, previous_value: OHLCV) -> bool:
        current_time_normalized = self._normalize(current_value.time)
        last_time_normalized = self._normalize(previous_value.time)

        return current_time_normalized == last_time_normalized

    def _normalize(self, dt: datetime):
        period_type = self.period_type.value[0]
        period_length = self.period_type.value[1]

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
