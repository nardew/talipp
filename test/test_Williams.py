import unittest

from talipp.indicators import Williams

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = Williams(14, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], -11.065573, places = 5)
        self.assertAlmostEqual(ind[-2], -25.819672, places = 5)
        self.assertAlmostEqual(ind[-1], -35.245901, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(Williams(14, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(Williams(14, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(Williams(143, self.input_values))


if __name__ == '__main__':
    unittest.main()
