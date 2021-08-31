import unittest
from datetime import datetime

from talipp.ohlcv import OHLCV, OHLCVFactory


class Test(unittest.TestCase):
    def test_from_matrix_w_volume(self):
        values = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 0]
        ]

        self.assertListEqual(OHLCVFactory.from_matrix(values),
                             [
                                 OHLCV(1, 2, 3, 4, 5),
                                 OHLCV(6, 7, 8, 9, 0),
                             ])

    def test_from_matrix_wo_volume(self):
        values = [
            [1, 2, 3, 4],
            [6, 7, 8, 9]
        ]

        self.assertListEqual(OHLCVFactory.from_matrix(values),
                             [
                                 OHLCV(1, 2, 3, 4, None),
                                 OHLCV(6, 7, 8, 9, None),
                             ])

    def test_from_matrix_w_time(self):
        now = datetime.now()
        values = [
            [1, 2, 3, 4, 5, now],
            [6, 7, 8, 9, 0, now]
        ]

        self.assertListEqual(OHLCVFactory.from_matrix(values),
                             [
                                 OHLCV(1, 2, 3, 4, 5, now),
                                 OHLCV(6, 7, 8, 9, 0, now),
                             ])

    def test_from_matrix2_w_volume(self):
        values = [
            [1, 6],
            [2, 7],
            [3, 8],
            [4, 9],
            [5, 0]
        ]

        self.assertListEqual(OHLCVFactory.from_matrix2(values),
                             [
                                 OHLCV(1, 2, 3, 4, 5),
                                 OHLCV(6, 7, 8, 9, 0),
                             ])

    def test_from_matrix2_wo_volume(self):
        values = [
            [1, 6],
            [2, 7],
            [3, 8],
            [4, 9]
        ]

        self.assertListEqual(OHLCVFactory.from_matrix2(values),
                             [
                                 OHLCV(1, 2, 3, 4, None),
                                 OHLCV(6, 7, 8, 9, None),
                             ])

    def test_from_matrix2_w_time(self):
        now = datetime.now()
        values = [
            [1, 6],
            [2, 7],
            [3, 8],
            [4, 9],
            [5, 0],
            [now, now]
        ]

        self.assertListEqual(OHLCVFactory.from_matrix2(values),
                             [
                                 OHLCV(1, 2, 3, 4, 5, now),
                                 OHLCV(6, 7, 8, 9, 0, now),
                             ])

    def test_from_dict_w_volume(self):
        values = {
            'open': [1, 6],
            'high': [2, 7],
            'low': [3, 8],
            'close': [4, 9],
            'volume': [5, 0]
        }

        self.assertListEqual(OHLCVFactory.from_dict(values),
                             [
                                 OHLCV(1, 2, 3, 4, 5),
                                 OHLCV(6, 7, 8, 9, 0),
                             ])

    def test_from_dict_wo_volume(self):
        values = {
            'open': [1, 6],
            'high': [2, 7],
            'low': [3, 8],
            'close': [4, 9]
        }

        self.assertListEqual(OHLCVFactory.from_dict(values),
                             [
                                 OHLCV(1, 2, 3, 4, None),
                                 OHLCV(6, 7, 8, 9, None),
                             ])

    def test_from_dict_w_time(self):
        now = datetime.now()
        values = {
            'open': [1, 6],
            'high': [2, 7],
            'low': [3, 8],
            'close': [4, 9],
            'volume': [5, 0],
            'time': [now, now]
        }

        self.assertListEqual(OHLCVFactory.from_dict(values),
                             [
                                 OHLCV(1, 2, 3, 4, 5, now),
                                 OHLCV(6, 7, 8, 9, 0, now),
                             ])


if __name__ == '__main__':
    unittest.main()
