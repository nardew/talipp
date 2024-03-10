import unittest

from talipp.indicators import ATR

from TalippTest import TalippTest


class TestATR(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = ATR(5, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.676426, places = 5)
        self.assertAlmostEqual(ind[-2], 0.665141, places = 5)
        self.assertAlmostEqual(ind[-1], 0.686113, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ATR(5, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ATR(5, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ATR(5, self.input_values))


if __name__ == '__main__':
    unittest.main()
