"""Collection of classes related to `OHLCV` input type."""

from dataclasses import dataclass
from datetime import datetime
from itertools import zip_longest
from typing import List, Dict, Optional


@dataclass
class OHLCV:
    """`OHLCV` input representation.

    Attributes:
        open: Open price.
        high: High price.
        low: Low price.
        close: Close price.
        volume: Volume.
        time: Timestamp.
    """

    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[float] = None
    time: Optional[datetime] = None


class OHLCVFactory:
    """Static class serving to create `OHLCV` input objects from various representations."""

    @staticmethod
    def from_matrix(values: List[List[float]]) -> List[OHLCV]:
        """Converts lists/tuples representing OHLCV values into a list of `OHLCV` objects.

        Expected dimension of input OHLCV list
        is 4 (without volume and timestamp), 5 (with volume and without timestamp) or 6 (with volume and timestamp).

        Examples:

            [[1,2,3,4,5], [6,7,8,9,0]] -> [OHLCV(1,2,3,4,5), OHLCV(6,7,8,9,0)]
            [[1,2,3,4], [6,7,8,9]] -> [OHLCV(1,2,3,4), OHLCV(6,7,8,9)]
            [[1,2,3,4,5,6], [7,8,9,10,11,12]] -> [OHLCV(1,2,3,4,5,6), OHLCV(7,8,9,10,11,12)]

        Args:
            values: A list of values to be converted into `OHLCV` objects.

        Returns:
            A list of `OHLCV` objects.
        """

        return [OHLCV(x[0],
                      x[1],
                      x[2],
                      x[3],
                      x[4] if len(x) >= 5 else None,
                      x[5] if len(x) >= 6 else None) for x in values]

    @staticmethod
    def from_matrix2(values: List[List[float]]) -> List[OHLCV]:
        """Converts lists representing O, H, L, C, V and T values into a list of `OHLCV` objects.

        Examples:

            [[1,2], [3,4], [5,6], [7,8]] -> [OHLCV(1,3,5,7), OHLCV(2,4,6,8)]
            [[1,2], [3,4], [5,6], [7,8], [9,0]] -> [OHLCV(1,3,5,7,9), OHLCV(2,4,6,8,0)]
            [[1,2], [3,4], [5,6], [7,8], [9,0], [11, 12]] -> [OHLCV(1,3,5,7,9,11), OHLCV(2,4,6,8,0,12)]

        Args:
            values: A list of values to be converted into `OHLCV` objects.

        Returns:
            A list of `OHLCV` objects.
        """

        if len(values) == 4:
            return OHLCVFactory.from_matrix(list(map(list, zip_longest(values[0],
                                                                       values[1],
                                                                       values[2],
                                                                       values[3]))))
        elif len(values) == 5:
            return OHLCVFactory.from_matrix(list(map(list, zip_longest(values[0],
                                                                       values[1],
                                                                       values[2],
                                                                       values[3],
                                                                       values[4]))))
        else:
            return OHLCVFactory.from_matrix(list(map(list, zip_longest(values[0],
                                                                       values[1],
                                                                       values[2],
                                                                       values[3],
                                                                       values[4],
                                                                       values[5]))))

    @staticmethod
    def from_dict(values: Dict[str, List[float]]) -> List[OHLCV]:
        """Converts a dict with OHLCV values into a list of `OHLCV` objects.

        The dict consists of `open`, `high`, `low`, `close`, `volume` and `time` keys where each key
        contains a list of simple values. If some key is missing, corresponding values
        in OHLCV will be None.

        Examples:

            {'open': [1,2], 'close': [3,4]} -> [OHLCV(1, None, None, 3, None, None), OHLCV(2, None, None, 4, None, None)]

        Args:
            values: A dict of values to be converted into `OHLCV` objects.

        Returns:
            A list of `OHLCV` objects.
        """

        return OHLCVFactory.from_matrix2([
            values['open'] if 'open' in values else [],
            values['high'] if 'high' in values else [],
            values['low'] if 'low' in values else [],
            values['close'] if 'close' in values else [],
            values['volume'] if 'volume' in values else [],
            values['time'] if 'time' in values else []
        ])


class ValueExtractor:
    """A set of static methods extracting attributes from `OHLCV` objects.

    The methods primarily serve as input modifiers in indicators.
    """

    @staticmethod
    def extract_open(value: OHLCV) -> float:
        """Extract open price.

        Args:
            value: `OHLCV` value

        Returns:
            Open price.
        """

        return value.open

    @staticmethod
    def extract_high(value: OHLCV) -> float:
        """Extract high price.

        Args:
            value: `OHLCV` value

        Returns:
            High price.
        """

        return value.high

    @staticmethod
    def extract_low(value: OHLCV) -> float:
        """Extract low price.

        Args:
            value: `OHLCV` value

        Returns:
            Low price.
        """

        return value.low

    @staticmethod
    def extract_close(value: OHLCV) -> float:
        """Extract close price.

        Args:
            value: `OHLCV` value

        Returns:
            Close price.
        """

        return value.close

    @staticmethod
    def extract_volume(value: OHLCV) -> float:
        """Extract volume.

        Args:
            value: `OHLCV` value

        Returns:
            Volume.
        """

        return value.volume
