from dataclasses import dataclass
from itertools import zip_longest
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class OHLCV:
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[float] = None
    time: Optional[datetime] = None


class OHLCVFactory:
    @staticmethod
    def from_matrix(values: List[List[float]]) -> List[OHLCV]:
        """
        Converts lists representing OHLCV values into lists of OHLCV objects. Expected dimension of input OHLCV list
        is 4 (without volume and timestamp), 5 (with volume and without timestamp) or 6 (with volume and timestamp).

        Unlike from_matrix2 in this method each input sublist represents an OHLCV tuple.

        Example: [[1,2,3,4,5], [6,7,8,9,0]] -> [OHLCV(1,2,3,4,5), OHLCV(6,7,8,9,0)]
        Example: [[1,2,3,4], [6,7,8,9]] -> [OHLCV(1,2,3,4), OHLCV(6,7,8,9)]
        Example: [[1,2,3,4,5,6], [7,8,9,10,11,12]] -> [OHLCV(1,2,3,4,5,6), OHLCV(7,8,9,10,11,12)]
        """
        return [OHLCV(x[0],
                      x[1],
                      x[2],
                      x[3],
                      x[4] if len(x) >= 5 else None,
                      x[5] if len(x) >= 6 else None) for x in values]

    @staticmethod
    def from_matrix2(values: List[List[float]]) -> List[OHLCV]:
        """
        Converts lists representing O, H, L, C, V and T(ime) values into lists of OHLCV objects.

        Unlike from_matrix in this method each input sublist represents all opens, highs, ...

        Example: [[1,2], [3,4], [5,6], [7,8]] -> [OHLCV(1,3,5,7), OHLCV(2,4,6,8)]
        Example: [[1,2], [3,4], [5,6], [7,8], [9,0]] -> [OHLCV(1,3,5,7,9), OHLCV(2,4,6,8,0)]
        Example: [[1,2], [3,4], [5,6], [7,8], [9,0], [11, 12]] -> [OHLCV(1,3,5,7,9,11), OHLCV(2,4,6,8,0,12)]
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
        """
        Converts a dict with keys 'open', 'high', 'low', 'close', 'volume' and 'time' where each key
        contains a list of simple values into a list of OHLCV objects. If some key is missing, corresponding values
        in OHLCV will be None

        Example: {'open': [1,2], 'close': [3,4]} -> [OHLCV(1, None, None, 3, None, None), OHLCV(2, None, None, 4, None, None)]
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
    @staticmethod
    def extract_open(value: OHLCV) -> float:
        return value.open

    @staticmethod
    def extract_high(value: OHLCV) -> float:
        return value.high

    @staticmethod
    def extract_low(value: OHLCV) -> float:
        return value.low

    @staticmethod
    def extract_close(value: OHLCV) -> float:
        return value.close

    @staticmethod
    def extract_volume(value: OHLCV) -> float:
        return value.volume
