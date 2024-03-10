import unittest

from talipp.indicators import VWAP

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = VWAP(self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[0], 10.47333, places = 5)
        self.assertAlmostEqual(ind[1], 10.21883, places = 5)
        self.assertAlmostEqual(ind[2], 10.20899, places = 5)
        self.assertAlmostEqual(ind[-3], 9.125770, places = 5)
        self.assertAlmostEqual(ind[-2], 9.136613, places = 5)
        self.assertAlmostEqual(ind[-1], 9.149069, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(VWAP(self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(VWAP(self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(VWAP(self.input_values))


if __name__ == '__main__':
    unittest.main()
