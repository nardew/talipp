import unittest

from talipp.ohlcv import OHLCV, OHLCVFactory


class TestOHLC(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
