import unittest

from talipp.indicators import WilderMA

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.CLOSE_TMPL)

    def test_init(self):
        ind = WilderMA(5, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 9.699400, places = 5)
        self.assertAlmostEqual(ind[-2], 9.805521, places = 5)
        self.assertAlmostEqual(ind[-1], 9.844417, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(WilderMA(5, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(WilderMA(5, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(WilderMA(5, self.input_values))


if __name__ == '__main__':
    unittest.main()
