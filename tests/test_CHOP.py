import unittest

from talipp.indicators import CHOP

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = CHOP(14, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 49.835100, places = 5)
        self.assertAlmostEqual(ind[-2], 50.001477, places = 5)
        self.assertAlmostEqual(ind[-1], 49.289273, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(CHOP(14, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(CHOP(14, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(CHOP(14, self.input_values))


if __name__ == '__main__':
    unittest.main()
