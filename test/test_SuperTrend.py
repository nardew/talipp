import unittest

from talipp.indicators import SuperTrend
from talipp.indicators.SuperTrend import Trend


from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = SuperTrend(10, 3, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-16].value, 9.711592, places = 5)
        self.assertAlmostEqual(ind[-16].trend, Trend.DOWN, places = 5)

        self.assertAlmostEqual(ind[-4].value, 8.110029, places = 5)
        self.assertAlmostEqual(ind[-4].trend, Trend.UP, places = 5)

        self.assertAlmostEqual(ind[-3].value, 8.488026, places = 5)
        self.assertAlmostEqual(ind[-3].trend, Trend.UP, places = 5)

        self.assertAlmostEqual(ind[-2].value, 8.488026, places = 5)
        self.assertAlmostEqual(ind[-2].trend, Trend.UP, places = 5)

        self.assertAlmostEqual(ind[-1].value, 8.488026, places = 5)
        self.assertAlmostEqual(ind[-1].trend, Trend.UP, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(SuperTrend(10, 3, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(SuperTrend(10, 3, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(SuperTrend(10, 3, self.input_values))


if __name__ == '__main__':
    unittest.main()
