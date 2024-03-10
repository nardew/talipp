import unittest

from talipp.indicators import AccuDist
from talipp.ohlcv import OHLCV

from TalippTest import TalippTest


class TestAccuDist(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = AccuDist(self.input_values)

        print(ind)
        self.assertAlmostEqual(ind[-3], -689.203568, places = 5)
        self.assertAlmostEqual(ind[-2], -725.031632, places = 5)
        self.assertAlmostEqual(ind[-1], -726.092152, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(AccuDist(self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(AccuDist(self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(AccuDist(self.input_values))

    def test_low_high_equal(self):
        ind = AccuDist(self.input_values)
        ind.add(OHLCV(1, 1, 1, 1, 1))

        # no assert since the check verifies no exception was raised


if __name__ == '__main__':
    unittest.main()
