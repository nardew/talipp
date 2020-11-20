import unittest

from talipp.indicators import Stoch

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = Stoch(14, 3, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].k, 88.934426, places = 5)
        self.assertAlmostEqual(ind[-3].d, 88.344442, places = 5)

        self.assertAlmostEqual(ind[-2].k, 74.180327, places = 5)
        self.assertAlmostEqual(ind[-2].d, 84.499789, places = 5)

        self.assertAlmostEqual(ind[-1].k, 64.754098, places = 5)
        self.assertAlmostEqual(ind[-1].d, 75.956284, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(Stoch(14, 3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(Stoch(14, 3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(Stoch(14, 3, self.input_values))


if __name__ == '__main__':
    unittest.main()
