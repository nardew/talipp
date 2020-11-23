import unittest

from talipp.indicators import ParabolicSAR
from talipp.indicators.ParabolicSAR import SARTrend

from TalippTest import TalippTest


class TestBB(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = ParabolicSAR(0.02, 0.02, 0.2, self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3].value, 8.075630, places = 5)
        self.assertAlmostEqual(ind[-3].trend, SARTrend.UP, places = 5)
        self.assertAlmostEqual(ind[-3].ep, 10.860000, places = 5)
        self.assertAlmostEqual(ind[-3].accel_factor, 0.060000, places = 5)

        self.assertAlmostEqual(ind[-2].value, 8.242693, places = 5)
        self.assertAlmostEqual(ind[-2].trend, SARTrend.UP, places = 5)
        self.assertAlmostEqual(ind[-2].ep, 10.860000, places = 5)
        self.assertAlmostEqual(ind[-2].accel_factor, 0.060000, places = 5)

        self.assertAlmostEqual(ind[-1].value, 8.399731, places = 5)
        self.assertAlmostEqual(ind[-1].trend, SARTrend.UP, places = 5)
        self.assertAlmostEqual(ind[-1].ep, 10.860000, places = 5)
        self.assertAlmostEqual(ind[-1].accel_factor, 0.060000, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(ParabolicSAR(0.02, 0.02, 0.2, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(ParabolicSAR(0.02, 0.02, 0.2, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(ParabolicSAR(0.02, 0.02, 0.2, self.input_values))


if __name__ == '__main__':
    unittest.main()
