import unittest

from talipp.indicators import RogersSatchell

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = RogersSatchell(9, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.036353, places = 5)
        self.assertAlmostEqual(ind[-2], 0.035992, places = 5)
        self.assertAlmostEqual(ind[-1], 0.040324, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(RogersSatchell(9, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(RogersSatchell(9, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(RogersSatchell(9, self.input_values))


if __name__ == '__main__':
    unittest.main()
