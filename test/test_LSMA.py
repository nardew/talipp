import unittest

from talipp.indicators import LSMA

from TalippTest import TalippTest


class TestLSMA(TalippTest):
    def setUp(self) -> None:
        self.input_values = TalippTest.TIMED_CLOSE_TMPL

    def test_init_with_period_2(self):
        ind = LSMA(2, self.input_values)

        self.assertAlmostEqual(ind[-3].slope, 0.29, places=5)
        self.assertAlmostEqual(ind[-3].intercept, 10.01, places=5)
        self.assertAlmostEqual(ind[-3].pred, 10.59, places=5)

        self.assertAlmostEqual(ind[-2].slope, -0.36, places=5)
        self.assertAlmostEqual(ind[-2].intercept, 10.95, places=5)
        self.assertAlmostEqual(ind[-2].pred, 10.23, places=5)

        self.assertAlmostEqual(ind[-1].slope, -0.23, places=5)
        self.assertAlmostEqual(ind[-1].intercept, 10.46, places=5)
        self.assertAlmostEqual(ind[-1].pred, 10.0, places=5)

    def test_init_with_period_5(self):
        ind = LSMA(5, self.input_values)

        self.assertAlmostEqual(ind[-3].slope, 0.529, places=5)
        self.assertAlmostEqual(ind[-3].intercept, 8.161, places=5)
        self.assertAlmostEqual(ind[-3].pred, 10.806, places=5)

        self.assertAlmostEqual(ind[-2].slope, 0.248, places=5)
        self.assertAlmostEqual(ind[-2].intercept, 9.352, places=5)
        self.assertAlmostEqual(ind[-2].pred, 10.592, places=5)

        self.assertAlmostEqual(ind[-1].slope, -0.037, places=5)
        self.assertAlmostEqual(ind[-1].intercept, 10.365, places=5)
        self.assertAlmostEqual(ind[-1].pred, 10.180, places=5)

    def test_update(self):
        self.assertIndicatorUpdate(LSMA(5, self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(LSMA(5, self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(LSMA(5, self.input_values))


if __name__ == "__main__":
    unittest.main()
