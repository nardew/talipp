import unittest

from talipp.indicators import BOP

from TalippTest import TalippTest


class Test(TalippTest):
    def setUp(self) -> None:
        self.input_values = list(TalippTest.OHLCV_TMPL)

    def test_init(self):
        ind = BOP(self.input_values)

        print(ind)

        self.assertAlmostEqual(ind[-3], 0.447761, places = 5)
        self.assertAlmostEqual(ind[-2], -0.870967, places = 5)
        self.assertAlmostEqual(ind[-1], -0.363636, places = 5)

    def test_update(self):
        self.assertIndicatorUpdate(BOP(self.input_values))

    def test_delete(self):
        self.assertIndicatorDelete(BOP(self.input_values))

    def test_purge_oldest(self):
        self.assertIndicatorPurgeOldest(BOP(self.input_values))


if __name__ == '__main__':
    unittest.main()
