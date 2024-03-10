import unittest

from talipp.indicators import ForceIndex

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = ForceIndex(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 24.015092, places = 5)
        self.assertAlmostEqual(ind[-2], 20.072283, places = 5)
        self.assertAlmostEqual(ind[-1], 16.371894, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ForceIndex(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ForceIndex(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ForceIndex(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
