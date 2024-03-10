import unittest
from datetime import datetime

from talipp.input import SamplingPeriodType, Sampler
from talipp.ohlcv import OHLCV


class Test(unittest.TestCase):
    @staticmethod
    def get_ohlcv(dt_str: str) -> OHLCV:
        return OHLCV(0, 0, 0, 0, 0,
                     datetime.strptime(dt_str, f"%d/%m/%Y %H:%M:%S{'.%f' if '.' in dt_str else ''}"))

    def test_sample_normalize_1sec(self):
        sampler = Sampler(SamplingPeriodType.SEC_1)

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:56.000000"),
                                               self.get_ohlcv("01/01/2024 12:34:56")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:56.123456"),
                                               self.get_ohlcv("01/01/2024 12:34:56.234567")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:56.999999"),
                                               self.get_ohlcv("01/01/2024 12:34:56")))

        self.assertFalse(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:56.999999"),
                                                self.get_ohlcv("01/01/2024 12:34:57")))

    def test_sample_normalize_3sec(self):
        sampler = Sampler(SamplingPeriodType.SEC_3)

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:00.100000"),
                                               self.get_ohlcv("01/01/2024 12:34:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:01.100000"),
                                               self.get_ohlcv("01/01/2024 12:34:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:02.100000"),
                                               self.get_ohlcv("01/01/2024 12:34:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:03.100000"),
                                               self.get_ohlcv("01/01/2024 12:34:03")))

        self.assertFalse(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:00"),
                                                self.get_ohlcv("01/01/2024 12:34:03")))

    def test_sample_normalize_5min(self):
        sampler = Sampler(SamplingPeriodType.MIN_5)

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:30:56.000000"),
                                               self.get_ohlcv("01/01/2024 12:30:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:56.000000"),
                                               self.get_ohlcv("01/01/2024 12:30:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:36:56.000000"),
                                               self.get_ohlcv("01/01/2024 12:35:00")))

        self.assertFalse(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:59"),
                                                self.get_ohlcv("01/01/2024 12:35:00")))

    def test_sample_normalize_1hour(self):
        sampler = Sampler(SamplingPeriodType.HOUR_1)

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 00:00:00.000000"),
                                               self.get_ohlcv("01/01/2024 00:00:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:00:00.000000"),
                                               self.get_ohlcv("01/01/2024 12:00:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:34:56.000000"),
                                               self.get_ohlcv("01/01/2024 12:00:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 13:36:56.000000"),
                                               self.get_ohlcv("01/01/2024 13:00:00")))

        self.assertFalse(sampler.is_same_period(self.get_ohlcv("01/01/2024 23:59:59"),
                                                self.get_ohlcv("02/01/2024 00:00:00")))

    def test_sample_normalize_1day(self):
        sampler = Sampler(SamplingPeriodType.DAY_1)

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 00:00:00.000000"),
                                               self.get_ohlcv("01/01/2024 00:00:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("01/01/2024 12:00:00.000000"),
                                               self.get_ohlcv("01/01/2024 00:00:00")))

        self.assertTrue(sampler.is_same_period(self.get_ohlcv("29/02/2024 12:34:56.000000"),
                                               self.get_ohlcv("29/02/2024 00:00:00")))

        self.assertFalse(sampler.is_same_period(self.get_ohlcv("01/01/2024 23:59:59"),
                                                self.get_ohlcv("02/01/2024 00:00:00")))


if __name__ == '__main__':
    unittest.main()
