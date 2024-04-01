import unittest

from talipp.indicators import SOBV

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = SOBV(20, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 90.868499, places = 5)
        self.assertAlmostEqual(ind[-2], 139.166499, places = 5)
        self.assertAlmostEqual(ind[-1], 187.558499, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(SOBV(20, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(SOBV(20, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(SOBV(20, self.input_values))


if __name__ == '__main__':
    unittest.main()
