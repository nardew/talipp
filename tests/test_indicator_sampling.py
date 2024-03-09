import unittest
from datetime import datetime

from TalippTest import TalippTest
from talipp.indicators import OBV
from talipp.input import SamplingPeriodType
from talipp.ohlcv import OHLCV


class Test(TalippTest):
    def test_sampling(self):
        obv = OBV(input_sampling=SamplingPeriodType.SEC_1)
        dt = datetime(2024, 1, 1, 0, 0, 0)

        obv.add(OHLCV(1, 1, 1, 1, 1, dt))
        self.assertEqual(len(obv), 1)

        dt = dt.replace(second=1)
        obv.add(OHLCV(1, 1, 1, 2, 2, dt))
        self.assertEqual(len(obv), 2)
        self.assertEqual(obv[-1], 3)

        dt = dt.replace(microsecond=1)
        obv.add(OHLCV(1, 1, 1, 3, 3, dt))
        self.assertEqual(len(obv), 2)
        self.assertEqual(obv[-1], 4)

        dt = dt.replace(microsecond=2)
        obv.add(OHLCV(1, 1, 1, 4, 4, dt))
        self.assertEqual(len(obv), 2)
        self.assertEqual(obv[-1], 5)

        dt = dt.replace(second=2)
        obv.add(OHLCV(1, 1, 1, 5, 5, dt))
        self.assertEqual(len(obv), 3)
        self.assertEqual(obv[-2], 5)
        self.assertEqual(obv[-1], 10)


if __name__ == '__main__':
    unittest.main()
