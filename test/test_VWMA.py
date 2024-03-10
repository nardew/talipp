import unittest

from talipp.indicators import VWMA

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = VWMA(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.320203, places = 5)
        self.assertAlmostEqual(ind[-2], 9.352602, places = 5)
        self.assertAlmostEqual(ind[-1], 9.457708, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(VWMA(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(VWMA(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(VWMA(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
